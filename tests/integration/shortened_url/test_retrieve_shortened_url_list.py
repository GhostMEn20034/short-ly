from datetime import datetime, UTC, timedelta
from typing import List
import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import User, ShortenedUrl
from src.schemes.auth.token_data import AuthTokens


class TestRetrieveShortenedUrlList:

    @pytest.mark.asyncio
    async def test_retrieve_url_list_default_case(
            self, async_client: AsyncClient, async_db: AsyncSession,
            prepopulated_urls: List[ShortenedUrl],tokens: AuthTokens, user: User,
    ):
        """
        The user must retrieve all of its shortened urls.
        """
        response = await async_client.get(f"/api/v1/urls/",
                                                 headers={"Authorization": f"Bearer {tokens.access_token}"},
                                                 )

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()

        assert response_data["pagination"]["total_items"] == len(prepopulated_urls)
        # Ensure all items belong to the user
        assert all(item["user_id"] == user.id for item in response_data["items"])

    @pytest.mark.asyncio
    async def test_retrieve_url_list_with_date_range_filter(
            self, async_client: AsyncClient, async_db: AsyncSession,
            prepopulated_urls: List[ShortenedUrl], tokens: AuthTokens, user: User,
    ):
        """
        The user must retrieve all of its shortened URLs where created_at within the specified date range.
        """
        ten_days_ago = datetime.now(UTC) - timedelta(days=10)
        five_days_ago = datetime.now(UTC) - timedelta(days=5)

        new_shortened_url = ShortenedUrl(
            friendly_name="Some Friendly Name",
            is_short_code_custom=True,
            short_code="some-short-code",
            long_url="https://www.example.com/",
            user_id=user.id,
            created_at=ten_days_ago,
        )
        async_db.add(new_shortened_url)
        await async_db.commit()


        response = await async_client.get(f"/api/v1/urls/",
                                          headers={"Authorization": f"Bearer {tokens.access_token}"},
                                          params={
                                              "date_from": (ten_days_ago - timedelta(days=1)).isoformat(),
                                              "date_to": five_days_ago.isoformat(),
                                          }
                                          )

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        # Ensure that count of items
        assert response_data["pagination"]["total_items"] == 1
        # Ensure all items belong to the user
        assert all(item["user_id"] == user.id for item in response_data["items"])

    @pytest.mark.asyncio
    async def test_retrieve_url_list_with_date_range_no_results(
            self, async_client: AsyncClient, async_db: AsyncSession,
            prepopulated_urls: List[ShortenedUrl], tokens: AuthTokens, user: User,
    ):
        """
        The user must retrieve 0 shortened URLs when no URLs fall within the specified date range.
        """
        ten_days_ago = datetime.now(UTC) - timedelta(days=10)

        new_shortened_url = ShortenedUrl(
            friendly_name="Some Friendly Name",
            is_short_code_custom=True,
            short_code="some-short-code",
            long_url="https://www.example.com/",
            user_id=user.id,
            created_at=ten_days_ago,
        )
        async_db.add(new_shortened_url)
        await async_db.commit()

        # Set date range that does NOT include the created shortened URL
        response = await async_client.get(
            "/api/v1/urls/",
            headers={"Authorization": f"Bearer {tokens.access_token}"},
            params={
                "date_from": (ten_days_ago + timedelta(days=1)).isoformat(),
                "date_to": (ten_days_ago + timedelta(days=3)).isoformat(),
            }
        )

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()

        # Ensure that no items are returned
        assert response_data["pagination"]["total_items"] == 0
        assert len(response_data["items"]) == 0
