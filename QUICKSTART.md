# Quick Start Guide

Get up and running with the web scraper in 3 minutes!

## Step 1: Install Dependencies

```bash
pip install fastapi httpx readability-lxml markdownify python-multipart uvicorn
```

## Step 2: Start the Server

```bash
uvicorn app.main:app --reload
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Step 3: Open in Browser

Navigate to: **http://localhost:8000**

## Step 4: Scrape URLs

1. Paste URLs in the text area (one per line). For example:
   ```
   https://www.apotheek.nl/medicijnen/paracetamol/
   https://en.wikipedia.org/wiki/Web_scraping
   example.com
   ```

2. Choose whether to extract main content only (recommended)

3. Click **"Scrape & Download"**

4. Your `scraped_pages.zip` will download automatically!

## What You Get

Open the zip file and you'll find markdown files like:
- `paracetamol.md`
- `web-scraping.md`
- `example-domain.md`

Each file contains:
- The page title as heading
- Source URL
- Clean, formatted markdown content

## Tips

- ✅ You can omit `http://` or `https://` - it's added automatically
- ✅ Scrape 50+ URLs at once
- ✅ The scraper handles errors gracefully (creates error.md files)
- ✅ Toggle content extraction for better results on some sites

## Troubleshooting

**Can't install dependencies?**
- Make sure you have Python 3.10+ installed
- Try: `python -m pip install --upgrade pip`

**Server won't start?**
- Port 8000 might be in use. Try: `uvicorn app.main:app --port 8001`

**URLs not scraping?**
- Check your internet connection
- Some sites may block automated access
- Try toggling the "Extract main content" checkbox

---

For detailed documentation, see [README.md](README.md)

