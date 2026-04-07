"""Utils for WebFetchTool matching src/tools/WebFetchTool/utils.ts"""
from typing import Dict, Any, Optional
import re
from urllib.parse import urlparse


def extract_links(html: str) -> list[str]:
    """Extract links from HTML."""
    pattern = r'href=["\']([^"\']+)["\']'
    return re.findall(pattern, html)


def extract_text(html: str) -> str:
    """Extract text from HTML."""
    # Remove script and style elements
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def validate_url(url: str) -> Dict[str, Any]:
    """Validate URL."""
    try:
        result = urlparse(url)
        return {
            "valid": bool(result.scheme and result.netloc),
            "scheme": result.scheme,
            "netloc": result.netloc,
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}


__all__ = ["extract_links", "extract_text", "validate_url"]