"""
Vercel serverless function entry point.
This wraps the FastAPI app for Vercel's serverless environment.
"""
from app.main import app

# Vercel expects a variable named 'app' or 'handler'
handler = app

