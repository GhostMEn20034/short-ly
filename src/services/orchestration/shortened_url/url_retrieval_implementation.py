from typing import Tuple

from .url_retrieval_abstract import AbstractUrlRetrievalOrchestrator
from src.services.shortened_url.abstract_url_service import AbstractURLService
from src.services.cache.abstract_cache import AbstractCacheService


class UrlRetrievalOrchestrator(AbstractUrlRetrievalOrchestrator):
    def __init__(self,
                 url_service: AbstractURLService,
                 cache_service: AbstractCacheService,
                 ):
        self._url_service = url_service
        self._cache_service = cache_service

    async def retrieve_url(self, short_code: str) -> Tuple[str, str]:
        cache_key = f"short_codes:{short_code}"

        long_url = await self._cache_service.get(cache_key)
        if long_url is None:
            long_url = await self._url_service.get_long_url(short_code)
            await self._cache_service.set(cache_key, str(long_url), ttl=3600)

            return str(long_url), "MISS"  # Cache miss

        return long_url, "HIT"  # Cache hit
