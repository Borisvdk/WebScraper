# Deployment Guide

## Deploying to Vercel

This web scraper can be deployed to Vercel with a few simple steps.

### Prerequisites

1. A Vercel account (free tier works great!)
2. Vercel CLI installed (optional but recommended)

### Method 1: Deploy via Vercel Dashboard (Easiest)

1. **Push to GitHub** (already done! ✅)
   - Your repo: https://github.com/Borisvdk/WebScraper

2. **Go to Vercel**
   - Visit: https://vercel.com/new
   - Sign in with your GitHub account

3. **Import Repository**
   - Click "Import Git Repository"
   - Select `Borisvdk/WebScraper`
   - Click "Import"

4. **Configure Project**
   - Project Name: `web-scraper` (or whatever you prefer)
   - Framework Preset: **Other**
   - Root Directory: `./` (leave as is)
   - Build Command: Leave empty
   - Output Directory: Leave empty
   - Install Command: `pip install -r requirements.txt`

5. **Deploy**
   - Click "Deploy"
   - Wait 1-2 minutes
   - Your app will be live at: `https://your-project.vercel.app`

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```
   
4. **Deploy to Production**
   ```bash
   vercel --prod
   ```

### Configuration Files

The following files have been added for Vercel deployment:

- **`vercel.json`** - Vercel configuration
- **`api/index.py`** - Serverless function entry point
- **`runtime.txt`** - Python version specification
- **`requirements.txt`** - Dependencies (already existed)

### Important Notes

#### ⚠️ Serverless Limitations

Vercel runs on AWS Lambda with some constraints:

1. **Execution Time**: 10 seconds (Hobby), 60 seconds (Pro)
   - For scraping many URLs, this might timeout
   - **Solution**: Limit to 3-5 URLs per request, or upgrade to Pro

2. **Memory**: 1024 MB (Hobby), configurable (Pro)
   - Should be fine for most use cases

3. **Response Size**: 4.5 MB max
   - Large zip files might exceed this
   - **Solution**: Scrape fewer URLs per batch

#### Recommended Settings for Vercel

Update `app/main.py` for production:

```python
# Reduce timeout for serverless
response = await client.get(url, timeout=10.0)  # was 30.0

# Reduce concurrency
semaphore = asyncio.Semaphore(3)  # was 5
```

### Testing After Deployment

1. Visit your Vercel URL: `https://your-project.vercel.app`
2. Paste 2-3 URLs (start small on serverless)
3. Click "Scrape & Download"
4. Download should start within 10 seconds

### Troubleshooting

#### "Function Execution Timeout"
- You're scraping too many URLs or they're too slow
- Reduce the number of URLs per request (3-5 max)
- Or upgrade to Vercel Pro for 60s timeout

#### "Response Size Too Large"
- The zip file exceeds 4.5 MB
- Scrape fewer URLs per batch
- Or consider alternative hosting (see below)

#### Static files not loading
- Check that `static/` directory is included in deployment
- Verify `vercel.json` routes are correct

### Alternative Hosting Options

If Vercel's serverless limitations are too restrictive:

#### 1. Railway (Recommended for this app)
- Supports long-running processes
- No 10-second timeout
- Free tier: 500 hours/month
- Deploy: https://railway.app

#### 2. Render
- Free tier with persistent servers
- No function timeouts
- Deploy: https://render.com

#### 3. Fly.io
- Free tier with persistent apps
- Great for Python apps
- Deploy: https://fly.io

#### 4. DigitalOcean App Platform
- $5/month for basic tier
- No serverless limitations
- Full control

### For Railway Deployment (Alternative)

Railway is better suited for this scraper since it doesn't have serverless limitations.

1. Visit: https://railway.app
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `Borisvdk/WebScraper`
6. Railway auto-detects Python and deploys
7. Add start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Environment Variables (if needed)

If you want to add configuration:

```bash
# Vercel Dashboard > Settings > Environment Variables
TIMEOUT=10
MAX_CONCURRENT=3
```

Then update `app/main.py` to read from environment variables.

### Continuous Deployment

Both Vercel and Railway support automatic deployments:
- Push to GitHub → Automatic deployment
- Every commit triggers a new build
- Preview deployments for pull requests

---

**Recommendation**: Try Vercel first (it's the easiest), but if you hit timeout issues with multiple URLs, switch to **Railway** for a better experience with this type of app.

