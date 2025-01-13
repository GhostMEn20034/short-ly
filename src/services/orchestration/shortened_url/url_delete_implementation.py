from fastapi import HTTPException, status

from src.models import User
from .url_delete_abstract import AbstractUrlDeleteOrchestrator
from src.services.cache.abstract_cache import AbstractCacheService
from src.services.shortened_url.abstract_url_service import AbstractURLService


class UrlDeleteOrchestrator(AbstractUrlDeleteOrchestrator):
    def __init__(self,
                 url_service: AbstractURLService,
                 cache_service: AbstractCacheService,
                 ):
        self._url_service = url_service
        self._cache_service = cache_service

    async def delete_url(self, short_code: str, owner: User):
        deleted = await self._url_service.delete_shortened_url(short_code, owner)
        if deleted:
            await self._cache_service.delete(f"short_codes:{short_code}")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return deleted
