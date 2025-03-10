from typing import List

import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession
from src.models.qr_code import QRCode
from src.schemes.auth.token_data import AuthTokens
from datetime import datetime, timedelta, UTC


class TestGetQRCodeList:

    @pytest.mark.asyncio
    async def test_get_qr_code_list_success(
            self, async_client: AsyncClient, async_db: AsyncSession,
            tokens: AuthTokens, prepopulated_qr_codes_for_first_user: List[QRCode]
    ):
        """
        Ensures that the QR code list returns the correct items with userId and total count matching
        the length of prepopulated_qr_codes.
        """
        # Send GET request to fetch the list of QR codes
        response = await async_client.get(
            "/api/v1/qr-codes/",
            headers={"Authorization": f"Bearer {tokens.access_token}"},
        )

        # Assert the response status code is 200 OK
        assert response.status_code == 200
        response_data = response.json()

        # Check the number of items in the response matches the length of prepopulated_qr_codes
        assert len(response_data["items"]) == len(prepopulated_qr_codes_for_first_user)

        # Ensure each item in the response has the correct userId
        for item in response_data["items"]:
            assert item["userId"] == prepopulated_qr_codes_for_first_user[0].user_id

        # Ensure pagination is correct
        assert response_data["pagination"]["current_page"] == 1
        assert response_data["pagination"]["page_size"] == 15
        assert response_data["pagination"]["total_items"] == len(prepopulated_qr_codes_for_first_user)
        assert response_data["pagination"]["total_pages"] == 1

    @pytest.mark.asyncio
    async def test_get_qr_code_list_with_date_range_filter(
            self, async_client: AsyncClient, async_db: AsyncSession,
            tokens: AuthTokens, prepopulated_qr_codes_for_first_user: List[QRCode]
    ):
        """
        Ensures that filtering by date range (date_from and date_to) works correctly for the `created_at` field.
        """
        # Set the datetime range for filtering
        now = datetime.now(UTC)
        date_from = now - timedelta(days=2)
        date_to = now

        # Send GET request to fetch the list of QR codes with date range filter
        response = await async_client.get(
            "/api/v1/qr-codes/",
            headers={"Authorization": f"Bearer {tokens.access_token}"},
            params={
                "date_from": date_from.isoformat(),
                "date_to": date_to.isoformat(),
            }
        )

        # Assert the response status code is 200 OK
        assert response.status_code == 200
        response_data = response.json()

        # Check that only QR codes created within the specified date range are returned
        for item in response_data["items"]:
            created_at = datetime.fromisoformat(item["createdAt"].replace("Z", "+00:00"))
            assert created_at >= date_from
            assert created_at <= date_to

    @pytest.mark.asyncio
    async def test_get_qr_code_list_no_results_in_date_range(
            self, async_client: AsyncClient, async_db: AsyncSession,
            tokens: AuthTokens, prepopulated_qr_codes_for_first_user: List[QRCode]
    ):
        """
        Ensures that no QR codes are returned if none are within the specified date range.
        """
        # Set the datetime range where no QR codes are expected to match
        now = datetime.now(UTC)
        date_from = now + timedelta(days=1)
        date_to = now + timedelta(days=2)

        # Send GET request to fetch the list of QR codes with date range filter
        response = await async_client.get(
            "/api/v1/qr-codes/",
            headers={"Authorization": f"Bearer {tokens.access_token}"},
            params={
                "date_from": date_from.isoformat(),
                "date_to": date_to.isoformat(),
            }
        )

        # Assert the response status code is 200 OK
        assert response.status_code == 200
        response_data = response.json()

        # Check that no items are returned
        assert len(response_data["items"]) == 0
        assert response_data["pagination"]["current_page"] == 1
        assert response_data["pagination"]["total_items"] == 0
        assert response_data["pagination"]["total_pages"] == 1
