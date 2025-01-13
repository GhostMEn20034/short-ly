from typing import Optional, Any, Dict
from redis.asyncio import Redis

from src.services.cache.abstract_cache import AbstractCacheService


class RedisCacheService(AbstractCacheService):

    def __init__(self, redis: Redis):
        self._redis = redis

    async def get(self, key: str) -> Optional[str]:
        return await self._redis.get(key)

    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        await self._redis.set(key, value, ex=ttl)

    async def get_object(self, key: str) -> Optional[Dict]:
        return await self._redis.hgetall(key)

    async def set_object(self, key: str, value: Dict, ttl: Optional[int] = None) -> None:
        await self._redis.hset(key, mapping=value)
        if ttl is not None:
            await self._redis.expire(key, ttl)

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)



