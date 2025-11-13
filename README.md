# Web Scraper

A simple web scraper that converts multiple URLs to markdown files and packages them as a zip download.

## Features

- 🌐 **Bulk URL scraping**: Paste multiple URLs at once
- 📝 **Markdown conversion**: Automatically converts HTML to clean markdown
- 🎯 **Content extraction**: Optionally extracts main content only (removes ads, navigation, etc.)
- 📦 **Zip download**: Downloads all scraped pages as a single zip file
- ⚡ **Async processing**: Fast concurrent URL fetching
- 🎨 **Modern UI**: Beautiful, responsive web interface

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Setup

1. Install dependencies:

```bash
pip install fastapi httpx readability-lxml markdownify python-multipart uvicorn
```

Or if you have `uv` installed:

```bash
uv sync
```

## Usage

1. Start the server:

```bash
python -m uvicorn app.main:app --reload
```

Or with uvicorn directly:

```bash
uvicorn app.main:app --reload
```

2. Open your browser and navigate to:

```
http://localhost:8000
```

3. Paste your URLs (one per line) into the textarea

4. Optionally toggle "Extract main content only" to clean the content

5. Click "Scrape & Download"

6. Your markdown files will be downloaded as `scraped_pages.zip`

## Example URLs to Test

You can test with these sample URLs:

```
https://www.apotheek.nl/medicijnen/paracetamol/
https://www.farmacotherapeutischkompas.nl/bladeren/preparaatteksten/p/paracetamol
https://en.wikipedia.org/wiki/Web_scraping
```

## How It Works

1. **URL Normalization**: Automatically adds `https://` if no scheme is provided
2. **Concurrent Fetching**: Uses async HTTP requests with connection pooling (max 5 concurrent)
3. **Content Extraction**: Uses readability-lxml to extract main content
4. **Markdown Conversion**: Converts HTML to markdown with proper formatting
5. **Error Handling**: Creates error markdown files for failed URLs
6. **Zip Packaging**: Bundles all markdown files into a single zip archive

## Project Structure

```
WebScraper/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI application and scraping logic
├── static/
│   └── index.html       # Frontend UI
├── pyproject.toml       # Project dependencies
├── .gitignore
└── README.md
```

## API Endpoints

### `POST /api/scrape`

Scrapes multiple URLs and returns a zip file.

**Request Body:**
```json
{
  "urls": ["https://example.com", "https://another.com"],
  "clean_content": true
}
```

**Response:**
- Content-Type: `application/zip`
- File: `scraped_pages.zip`

### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Configuration

You can customize the scraper behavior in `app/main.py`:

- **Timeout**: Default 30 seconds (line ~55)
- **Max concurrent requests**: Default 5 (line ~125)
- **Max filename length**: Default 50 characters (line ~23)
- **Connection limits**: Max 10 connections, 5 keepalive (line ~121)

## Troubleshooting

### Server won't start

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

Or reinstall:
```bash
pip install fastapi httpx readability-lxml markdownify python-multipart uvicorn
```

### URLs not scraping

- Check that URLs are valid and accessible
- Some websites may block automated requests
- Check firewall/antivirus settings

### Markdown formatting issues

Toggle the "Extract main content only" option. Some websites work better with or without content extraction.

## Testing

### Manual Testing

1. Start the server as described in the Usage section
2. Open http://localhost:8000 in your browser
3. Paste some test URLs (one per line):
   ```
   https://www.apotheek.nl/medicijnen/paracetamol/
   https://en.wikipedia.org/wiki/Web_scraping
   https://example.com
   ```
4. Click "Scrape & Download"
5. Verify the zip file downloads and contains markdown files

### Automated Testing

A test script is provided in `test_scraper.py`. To run it:

1. Install the requests library:
   ```bash
   pip install requests
   ```

2. Make sure the server is running in another terminal:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Run the tests:
   ```bash
   python test_scraper.py
   ```

The test suite will verify:
- Health check endpoint
- Single URL scraping
- Multiple URL scraping
- Invalid URL handling
- Empty URL list validation

## Technical Details

- **Backend**: FastAPI (Python)
- **HTTP Client**: httpx (async)
- **HTML Parsing**: readability-lxml, lxml
- **Markdown Conversion**: markdownify
- **Concurrency**: asyncio with semaphores

## License

MIT License - feel free to use and modify as needed.

