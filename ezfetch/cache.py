"""
Caching system for expensive operations
"""
import json
import time
from pathlib import Path
from typing import Any, Optional, Callable
from functools import wraps


class Cache:
    """Simple file-based cache for system info"""

    def __init__(self, cache_dir: Optional[Path] = None, duration: int = 300):
        self.cache_dir = cache_dir or (Path.home() / ".cache" / "ezfetch")
        self.duration = duration
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired"""
        cache_file = self.cache_dir / f"{key}.json"
        if not cache_file.exists():
            return None

        try:
            with open(cache_file, "r") as f:
                data = json.load(f)
            
            if time.time() - data.get("timestamp", 0) < self.duration:
                return data.get("value")
        except (json.JSONDecodeError, IOError):
            pass

        return None

    def set(self, key: str, value: Any) -> None:
        """Cache a value with timestamp"""
        cache_file = self.cache_dir / f"{key}.json"
        try:
            with open(cache_file, "w") as f:
                json.dump({
                    "timestamp": time.time(),
                    "value": value
                }, f)
        except IOError:
            pass

    def clear(self, key: Optional[str] = None) -> None:
        """Clear specific key or all cache"""
        if key:
            cache_file = self.cache_dir / f"{key}.json"
            if cache_file.exists():
                cache_file.unlink()
        else:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()


# Global cache instance
_cache_instance: Optional[Cache] = None


def get_cache(duration: int = 300) -> Cache:
    """Get or create global cache instance"""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = Cache(duration=duration)
    return _cache_instance


def cached(key: str, duration: int = 300):
    """Decorator to cache function results"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = get_cache(duration)
            cached_value = cache.get(key)
            if cached_value is not None:
                return cached_value
            
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        return wrapper
    return decorator
