from typing import List
from unittest import mock

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.containers import Container
from src.models import ShortenedUrl
from src.schemes.auth.token_data import AuthTokens
from src.services.cache.cache_stub import CacheServiceStub


class TestDeleteShortenedUrl:

    @pytest.mark.asyncio
    async def test_delete_url_default_case(
            self, app: FastAPI, async_client: AsyncClient, async_db: AsyncSession,
            prepopulated_urls: List[ShortenedUrl], tokens: AuthTokens,
    ):
        """
        If the user is owner of the url and url exists, then everything should be deleted.
        Also, cache must be invalidated after the url delete.
        """
        mocked_cache_service = mock.AsyncMock(spec=CacheServiceStub)
        mocked_cache_service.delete.return_value = None

        container: Container = app.container

        with container.redis_cache_service.override(mocked_cache_service):
            response = await async_client.delete(f"/api/v1/urls/{prepopulated_urls[0].short_code}",
                                              headers={"Authorization": f"Bearer {tokens.access_token}"},
                                              )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Ensure that cache was invalidated
        mocked_cache_service.delete.assert_called_with(f"short_codes:{prepopulated_urls[0].short_code}")

    @pytest.mark.asyncio
    async def test_delete_non_existing_url(self, async_client: AsyncClient, tokens: AuthTokens):
        """
        If a user trying to delete non-existing url, the user will get HTTP 404 NOT FOUND error.
        """
        response = await async_client.delete("/api/v1/urls/dasds314",
                                          headers={"Authorization": f"Bearer {tokens.access_token}"},
                                          )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_delete_someone_else_url(
            self, async_client: AsyncClient, prepopulated_url_for_second_user: ShortenedUrl, tokens: AuthTokens,
    ):
        """
        If User 1 try to delete URL of User 2, User 1 must get HTTP 403 FORBIDDEN error.
        """
        response = await async_client.delete(f"/api/v1/urls/{prepopulated_url_for_second_user.short_code}",
                                          headers={"Authorization": f"Bearer {tokens.access_token}"},
                                          )

        assert response.status_code == status.HTTP_403_FORBIDDEN

        response_data = response.json()

        assert response_data["detail"] == "You are not the owner of this shortened url"
