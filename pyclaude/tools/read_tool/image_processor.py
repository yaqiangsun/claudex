"""Image processor for FileReadTool matching src/tools/FileReadTool/imageProcessor.ts"""
from typing import Dict, Any, Optional
import base64
import os


def is_image_file(path: str) -> bool:
    """Check if file is an image."""
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg'}
    ext = os.path.splitext(path)[1].lower()
    return ext in image_extensions


def encode_image_base64(path: str) -> Optional[str]:
    """Encode image as base64."""
    try:
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception:
        return None


def get_image_info(path: str) -> Dict[str, Any]:
    """Get image file information."""
    if not os.path.exists(path):
        return {"valid": False, "error": "File not found"}

    size = os.path.getsize(path)
    ext = os.path.splitext(path)[1].lower()

    return {
        "valid": True,
        "path": path,
        "size": size,
        "extension": ext,
        "is_image": is_image_file(path),
    }


__all__ = ["is_image_file", "encode_image_base64", "get_image_info"]