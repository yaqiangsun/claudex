"""
Memoize utility.
"""
from functools import lru_cache

def memoize(func=None, maxsize=128):
    if func is None:
        return lambda f: lru_cache(maxsize=maxsize)(f)
    return lru_cache(maxsize=maxsize)(func)

__all__ = ['memoize']