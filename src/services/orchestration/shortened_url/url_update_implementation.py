from src.models import User, ShortenedUrl
from src.schemes.shortened_url.request_bodies.update import UpdateShortenedUrlSchema

from .url_update_abstract import AbstractUrlUpdateOrchestrator
from src.services.shortened_url.abstract_url_service import AbstractURLService
from src.services.cache.abstract_cache import AbstractCacheService


class UrlUpdateOrchestrator(AbstractUrlUpdateOrchestrator):

    def __init__(self,
                 url_service: AbstractURLService,
                 cache_service: AbstractCacheService,
                 ):
        self._url_service = url_service
        self._cache_service = cache_service

    async def update_url(self, short_code: str, data: UpdateShortenedUrlSchema, owner: User) -> ShortenedUrl:
        """
        Updates shortened url information and invalidates cache
        """
        updated_url = await self._url_service.update_shortened_url(short_code, data, owner)

        await self._cache_service.delete(f"short_codes:{updated_url.short_code}")

        return updated_url