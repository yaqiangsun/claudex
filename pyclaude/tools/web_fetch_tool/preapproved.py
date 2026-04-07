"""Preapproved URLs matching src/tools/WebFetchTool/preapproved.ts"""
from typing import List

# Preapproved domains for web fetch
PREAPPROVED_DOMAINS = [
    "github.com",
    "gitlab.com",
    "bitbucket.org",
    "npmjs.com",
    "pypi.org",
    "docs.python.org",
    "developer.mozilla.org",
    "stackoverflow.com",
    "wikipedia.org",
    "medium.com",
    "dev.to",
    "huggingface.co",
    "arxiv.org",
    "paperswithcode.com",
]


def is_domain_preapproved(url: str) -> bool:
    """Check if URL domain is preapproved."""
    from urllib.parse import urlparse
    try:
        domain = urlparse(url).netloc
        return any(preapproved in domain for preapproved in PREAPPROVED_DOMAINS)
    except Exception:
        return False


def get_preapproved_domains() -> List[str]:
    """Get list of preapproved domains."""
    return PREAPPROVED_DOMAINS.copy()


__all__ = ["PREAPPROVED_DOMAINS", "is_domain_preapproved", "get_preapproved_domains"]