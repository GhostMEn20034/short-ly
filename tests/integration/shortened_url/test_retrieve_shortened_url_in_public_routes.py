from typing import List
from unittest import mock
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.containers import Container
from src.models import ShortenedUrl
from src.services.cache.cache_stub import CacheServiceStub
from src.services.shortened_url.url_service import URLService


class TestRetrieveShortenedUrlInPublicRoutes:
    @pytest.mark.asyncio
    async def test_retrieve_url_default_case(
            self, app: FastAPI, async_client: AsyncClient, async_db: AsyncSession,
            prepopulated_urls: List[ShortenedUrl],
    ):
        """
        If the url exists user must get redirect response ( HTTP 307 ) to long url.
        After first url retrieval long url must be saved to the cache in format: "short_codes:<short_code>":"<long_url>"
        """
        mocked_cache_service = mock.AsyncMock(spec=CacheServiceStub)
        mocked_cache_service.get.return_value = None
        mocked_cache_service.set.return_value = None

        container: Container = app.container

        with container.redis_cache_service.override(mocked_cache_service):
            response = await async_client.get(f"/{prepopulated_urls[0].short_code}")

        mocked_cache_service.get.assert_called_with(f"short_codes:{prepopulated_urls[0].short_code}")
        mocked_cache_service.set.assert_called_with(
            f"short_codes:{prepopulated_urls[0].short_code}",
            str(prepopulated_urls[0].long_url), ttl=3600,
        )

        # Make sure that we get redirect response
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

        # And make sure that we get redirect with the correct url
        redirect_url = response.headers.get("location")
        assert redirect_url == str(prepopulated_urls[0].long_url)

    @pytest.mark.asyncio
    async def test_retrieve_url_second_request_should_get_url_from_cache(
            self, app: FastAPI, async_client: AsyncClient, async_db: AsyncSession,
            prepopulated_urls: List[ShortenedUrl],
    ):
        """
        If long url is requested not for a first time, it must be queried from cache
        """
        response = await async_client.get(f"/{prepopulated_urls[0].short_code}")

        # Make sure that we get redirect response
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

        mocked_url_service = mock.AsyncMock(spec=URLService)
        mocked_url_service.get_long_url.return_value = None

        container: Container = app.container

        with container.url_service.override(mocked_url_service):
            response = await async_client.get(f"/{prepopulated_urls[0].short_code}")

        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert mocked_url_service.get_long_url.call_count == 0

    @pytest.mark.asyncio
    async def test_retrieve_non_existing_url(
            self, async_client: AsyncClient, async_db: AsyncSession,
            prepopulated_urls: List[ShortenedUrl]
    ):
        response = await async_client.get("/dfgfdgfer4")
        assert response.status_code == status.HTTP_404_NOT_FOUND