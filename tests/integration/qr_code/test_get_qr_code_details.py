from typing import List

import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession
from src.models.qr_code import QRCode
from src.schemes.auth.token_data import AuthTokens


class TestGetQRCodeDetails:
    @pytest.mark.asyncio
    async def test_get_qr_code_details_success(
            self, async_client: AsyncClient, async_db: AsyncSession,
            tokens: AuthTokens, prepopulated_qr_codes_for_first_user: List[QRCode]
    ):
        """
        Ensures that the QR code details are returned successfully when the user is the owner.
        """
        qr_code = prepopulated_qr_codes_for_first_user[0]

        # Send GET request to fetch the QR code details
        response = await async_client.get(
            f"/api/v1/qr-codes/{qr_code.id}",
            headers={"Authorization": f"Bearer {tokens.access_token}"},
        )

        # Assert the response status code is 200 OK
        assert response.status_code == 200
        response_data = response.json()

        # Check the response data against the expected structure
        assert response_data["id"] == qr_code.id
        assert response_data["title"] == qr_code.title
        assert response_data["userId"] == qr_code.user_id
        assert response_data["linkId"] == qr_code.link_id
        assert response_data["customization"] == qr_code.customization
        assert "createdAt" in response_data
        assert "updatedAt" in response_data
        assert response_data["link"]["friendly_name"] == qr_code.link.friendly_name
        assert response_data["link"]["short_code"] == qr_code.link.short_code
        assert response_data["link"]["long_url"] == qr_code.link.long_url

    @pytest.mark.asyncio
    async def test_get_qr_code_details_not_found(
            self, async_client: AsyncClient, tokens: AuthTokens
    ):
        """
        Ensures that if the QR code is not found, it returns a 404 Not Found status.
        """
        non_existing_qr_code_id = 9999

        response = await async_client.get(
            f"/api/v1/qr-codes/{non_existing_qr_code_id}",
            headers={"Authorization": f"Bearer {tokens.access_token}"},
        )

        # Assert the response status code is 404 Not Found
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_qr_code_details_not_owner(
            self, async_client: AsyncClient, async_db: AsyncSession,
            tokens: AuthTokens, prepopulated_qr_codes_for_second_user: List[QRCode]
    ):
        """
        Ensures that if the user is not the owner of the QR code, they receive a 403 Forbidden status.
        """
        qr_code = prepopulated_qr_codes_for_second_user[0]

        response = await async_client.get(
            f"/api/v1/qr-codes/{qr_code.id}",
            headers={"Authorization": f"Bearer {tokens.access_token}"},
        )

        # Assert the response status code is 403 Forbidden
        assert response.status_code == 403
