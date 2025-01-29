from typing import List
from fastapi import status, FastAPI
import pytest
from unittest import mock
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.containers import Container
from src.services.cache.cache_stub import CacheServiceStub
from src.models import ShortenedUrl
from src.schemes.auth.token_data import AuthTokens
from src.schemes.shortened_url.request_bodies.update import UpdateShortenedUrlSchema


class TestUpdateShortenedUrl:

    @pytest.mark.asyncio
    async def test_update_url_default_case(
        self, app: FastAPI, async_client: AsyncClient, async_db: AsyncSession,
            prepopulated_urls: List[ShortenedUrl], tokens: AuthTokens,
    ):
        """
        Default case. If request body is correct, then user can successfully update the shortened url's data.
        Also, the cache must be invalidated.
        """
        mocked_cache_service = mock.AsyncMock(spec=CacheServiceStub)
        mocked_cache_service.delete.return_value = None

        request_body = UpdateShortenedUrlSchema(
            friendly_name="New Friendly name",
            long_url="https://example.com",
        )

        serialized_body = request_body.model_dump()
        serialized_body["long_url"] = str(serialized_body["long_url"])

        container: Container = app.container

        with container.redis_cache_service.override(mocked_cache_service):
            response = await async_client.put(f"/api/v1/urls/{prepopulated_urls[0].short_code}",
                                           headers={"Authorization": f"Bearer {tokens.access_token}"},
                                           json=serialized_body,
                                           )

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        # Ensure that new data has applied to shortened url record
        assert response_data["friendly_name"] == request_body.friendly_name
        assert response_data["long_url"] == str(request_body.long_url)

        # Ensure that cache was invalidated
        mocked_cache_service.delete.assert_called_with(f"short_codes:{prepopulated_urls[0].short_code}")

    @pytest.mark.asyncio
    async def test_update_non_existing_url(self, async_client: AsyncClient, tokens: AuthTokens):
        """
        If a user trying to update non-existing url, the user will get HTTP 404 NOT FOUND error.
        """
        request_body = UpdateShortenedUrlSchema(
            friendly_name="New Friendly name",
            long_url="https://example.com",
        )

        serialized_body = request_body.model_dump()
        serialized_body["long_url"] = str(serialized_body["long_url"])

        response = await async_client.put("/api/v1/urls/dasds314",
                                          headers={"Authorization": f"Bearer {tokens.access_token}"},
                                          json=serialized_body,
                                          )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_update_someone_else_url(
            self, async_client: AsyncClient, prepopulated_url_for_second_user: ShortenedUrl, tokens: AuthTokens,
    ):
        """
        If User 1 try to update URL of User 2, User 1 must get HTTP 403 FORBIDDEN error.
        """
        request_body = UpdateShortenedUrlSchema(
            friendly_name="New Friendly name",
            long_url="https://example.com",
        )

        serialized_body = request_body.model_dump()
        serialized_body["long_url"] = str(serialized_body["long_url"])

        response = await async_client.put(f"/api/v1/urls/{prepopulated_url_for_second_user.short_code}",
                                          headers={"Authorization": f"Bearer {tokens.access_token}"},
                                          json=serialized_body,
                                          )

        assert response.status_code == status.HTTP_403_FORBIDDEN

        response_data = response.json()

        assert response_data["detail"] == "You are not the owner of this shortened url"
