import asyncio
import io
import re
import zipfile
from typing import List
from urllib.parse import urlparse

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from markdownify import markdownify as md
from pydantic import BaseModel
from readability import Document


app = FastAPI(title="Web Scraper")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


class ScrapeRequest(BaseModel):
    urls: List[str]
    clean_content: bool = True


def slugify(text: str, max_length: int = 50) -> str:
    """Convert text to a safe filename slug."""
    # Remove or replace unsafe characters
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    text = text.strip('-')
    return text[:max_length] if text else "page"


def normalize_url(url: str) -> str:
    """Add https:// if no scheme is present."""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url


async def fetch_and_convert(client: httpx.AsyncClient, url: str, clean_content: bool = True) -> tuple[str, str, str]:
    """
    Fetch a URL and convert to markdown.
    Returns: (url, filename, markdown_content)
    """
    try:
        # Normalize URL
        url = normalize_url(url)
        
        # Fetch with timeout and retries
        response = await client.get(
            url,
            timeout=30.0,
            follow_redirects=True,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        response.raise_for_status()
        
        html_content = response.text
        
        # Extract main content if requested
        if clean_content:
            doc = Document(html_content)
            title = doc.title()
            content_html = doc.summary()
        else:
            # Try to extract title from HTML
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
            title = title_match.group(1).strip() if title_match else urlparse(url).netloc
            content_html = html_content
        
        # Convert to markdown
        markdown_content = md(content_html, heading_style="ATX")
        
        # Prepend title and source URL
        markdown_output = f"# {title}\n\n**Source:** {url}\n\n---\n\n{markdown_content}"
        
        # Generate filename from title
        filename = slugify(title) + ".md"
        
        return url, filename, markdown_output
        
    except httpx.HTTPStatusError as e:
        error_msg = f"# Error fetching URL\n\n**URL:** {url}\n\n**Error:** HTTP {e.response.status_code}\n\n{str(e)}"
        filename = slugify(urlparse(url).netloc + "-error") + ".md"
        return url, filename, error_msg
        
    except Exception as e:
        error_msg = f"# Error fetching URL\n\n**URL:** {url}\n\n**Error:** {type(e).__name__}\n\n{str(e)}"
        filename = slugify(urlparse(url).netloc + "-error") + ".md"
        return url, filename, error_msg


@app.get("/")
async def root():
    """Serve the frontend."""
    return FileResponse("static/index.html")


@app.post("/api/scrape")
async def scrape_urls(request: ScrapeRequest):
    """
    Scrape multiple URLs and return as a zip file.
    """
    if not request.urls:
        raise HTTPException(status_code=400, detail="No URLs provided")
    
    # Filter out empty URLs
    urls = [url.strip() for url in request.urls if url.strip()]
    
    if not urls:
        raise HTTPException(status_code=400, detail="No valid URLs provided")
    
    # Create HTTP client with connection pooling
    async with httpx.AsyncClient(
        limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
    ) as client:
        # Fetch all URLs concurrently with semaphore to limit concurrency
        semaphore = asyncio.Semaphore(5)  # Max 5 concurrent requests
        
        async def fetch_with_limit(url: str):
            async with semaphore:
                return await fetch_and_convert(client, url, request.clean_content)
        
        results = await asyncio.gather(
            *[fetch_with_limit(url) for url in urls],
            return_exceptions=False
        )
    
    # Create zip file in memory
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Track filenames to avoid duplicates
        filename_counts = {}
        
        for url, filename, content in results:
            # Handle duplicate filenames
            if filename in filename_counts:
                filename_counts[filename] += 1
                name, ext = filename.rsplit('.', 1)
                filename = f"{name}-{filename_counts[filename]}.{ext}"
            else:
                filename_counts[filename] = 0
            
            # Add file to zip
            zip_file.writestr(filename, content)
    
    # Prepare zip for download
    zip_buffer.seek(0)
    
    return StreamingResponse(
        io.BytesIO(zip_buffer.read()),
        media_type="application/zip",
        headers={
            "Content-Disposition": "attachment; filename=scraped_pages.zip"
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

