"""Upload matching src/tools/BriefTool/upload.ts"""
from typing import Dict, Any, List, Optional
import os
import hashlib


def compute_file_hash(path: str) -> str:
    """Compute SHA256 hash of file."""
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def upload_file(path: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Upload a file for brief analysis."""
    if not os.path.exists(path):
        return {
            "success": False,
            "error": f"File not found: {path}",
        }

    file_hash = compute_file_hash(path)
    file_size = os.path.getsize(path)

    return {
        "success": True,
        "path": path,
        "hash": file_hash,
        "size": file_size,
        "metadata": metadata or {},
    }


def upload_multiple(paths: List[str]) -> List[Dict[str, Any]]:
    """Upload multiple files."""
    results = []
    for path in paths:
        results.append(upload_file(path))
    return results


__all__ = ["compute_file_hash", "upload_file", "upload_multiple"]