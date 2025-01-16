from typing import List
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import ShortenedUrl
from src.schemes.auth.token_data import AuthTokens


class TestRetrieveShortenedUrl:

    @pytest.mark.asyncio
    async def test_retrieve_url_default_case(
            self, app: FastAPI, async_client: AsyncClient, async_db: AsyncSession,
            prepopulated_urls: List[ShortenedUrl], tokens: AuthTokens,
    ):
        """
        If the user is owner of the url and url exists, then the url will be retrieved.
        """
        response = await async_client.get(f"/api/v1/urls/{prepopulated_urls[0].short_code}",
                                                 headers={"Authorization": f"Bearer {tokens.access_token}"},
                                                 )

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()

        assert response_data["id"] == prepopulated_urls[0].id

    @pytest.mark.asyncio
    async def test_retrieve_non_existing_url(
            self, async_client: AsyncClient, tokens: AuthTokens,
    ):
        response = await async_client.get("/api/v1/urls/dasds314",
                                             headers={"Authorization": f"Bearer {tokens.access_token}"},
                                             )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_retrieve_someone_else_url(
            self, async_client: AsyncClient, prepopulated_url_for_second_user: ShortenedUrl, tokens: AuthTokens,
    ):
        """
        If User 1 try to retrieve details of the URL of User 2, User 1 must get HTTP 403 FORBIDDEN error.
        """
        response = await async_client.delete(f"/api/v1/urls/{prepopulated_url_for_second_user.short_code}",
                                             headers={"Authorization": f"Bearer {tokens.access_token}"},
                                             )

        assert response.status_code == status.HTTP_403_FORBIDDEN

        response_data = response.json()

        assert response_data["detail"] == "You are not the owner of this shortened url"
