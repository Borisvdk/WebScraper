"""
Simple test script to verify web scraper functionality.
Run this after starting the server with: uvicorn app.main:app --reload
"""

import requests
import zipfile
import io


def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check endpoint...")
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("✓ Health check passed")


def test_scrape_single_url():
    """Test scraping a single URL."""
    print("\nTesting single URL scraping...")
    
    test_url = "https://example.com"
    payload = {
        "urls": [test_url],
        "clean_content": True
    }
    
    response = requests.post(
        "http://localhost:8000/api/scrape",
        json=payload,
        timeout=60
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"
    
    # Verify zip contents
    zip_buffer = io.BytesIO(response.content)
    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
        files = zip_file.namelist()
        assert len(files) == 1
        assert files[0].endswith('.md')
        
        # Read the markdown content
        content = zip_file.read(files[0]).decode('utf-8')
        assert "Source:" in content
        assert test_url in content
        
    print(f"✓ Single URL scraping passed (file: {files[0]})")


def test_scrape_multiple_urls():
    """Test scraping multiple URLs."""
    print("\nTesting multiple URL scraping...")
    
    test_urls = [
        "https://example.com",
        "https://example.org",
    ]
    payload = {
        "urls": test_urls,
        "clean_content": True
    }
    
    response = requests.post(
        "http://localhost:8000/api/scrape",
        json=payload,
        timeout=60
    )
    
    assert response.status_code == 200
    
    # Verify zip contains multiple files
    zip_buffer = io.BytesIO(response.content)
    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
        files = zip_file.namelist()
        assert len(files) == len(test_urls)
        
    print(f"✓ Multiple URL scraping passed ({len(files)} files created)")


def test_invalid_url_handling():
    """Test handling of invalid URLs."""
    print("\nTesting invalid URL handling...")
    
    payload = {
        "urls": ["https://this-is-not-a-real-domain-12345.com"],
        "clean_content": True
    }
    
    response = requests.post(
        "http://localhost:8000/api/scrape",
        json=payload,
        timeout=60
    )
    
    # Should still return a zip with error file
    assert response.status_code == 200
    
    zip_buffer = io.BytesIO(response.content)
    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
        files = zip_file.namelist()
        assert len(files) == 1
        
        # Read error content
        content = zip_file.read(files[0]).decode('utf-8')
        assert "Error" in content
        
    print("✓ Invalid URL handling passed")


def test_empty_urls():
    """Test with empty URL list."""
    print("\nTesting empty URL list...")
    
    payload = {
        "urls": [],
        "clean_content": True
    }
    
    response = requests.post(
        "http://localhost:8000/api/scrape",
        json=payload,
        timeout=60
    )
    
    assert response.status_code == 400
    print("✓ Empty URL list validation passed")


if __name__ == "__main__":
    print("=" * 60)
    print("Web Scraper Test Suite")
    print("=" * 60)
    print("\nMake sure the server is running:")
    print("  uvicorn app.main:app --reload")
    print("\nNote: You need 'requests' installed:")
    print("  pip install requests")
    print("=" * 60)
    
    try:
        test_health_check()
        test_scrape_single_url()
        test_scrape_multiple_urls()
        test_invalid_url_handling()
        test_empty_urls()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to server.")
        print("Make sure the server is running on http://localhost:8000")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")

