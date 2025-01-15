from typing import Dict, Optional

from .abstract_cache import AbstractCacheService


class CacheServiceStub(AbstractCacheService):
    """
    The class used to Imitate the cache service
    """
    def __init__(self):
        self._values = {}

    async def get(self, key: str) -> Optional[str]:
        return self._values.get(key)

    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        self._values[key] = value

    async def get_object(self, key: str) -> Optional[Dict]:
        return self._values.get(key)

    async def set_object(self, key: str, value: Dict, ttl: Optional[int] = None) -> None:
        self._values[key] = value

    async def delete(self, key: str) -> None:
        self._values.pop(key, None)
