import pytest
from typing import List
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.qr_code import QRCode
from src.schemes.auth.token_data import AuthTokens


class TestUpdateQRCode:

    @pytest.mark.asyncio
    async def test_update_qr_code_content(
            self, async_client: AsyncClient, async_db: AsyncSession,
            tokens: AuthTokens, prepopulated_qr_codes_for_first_user: List[QRCode],
    ):
        """
        Ensures that the title of the first prepopulated QR code is successfully updated using a PUT request.
        """
        qr_code = prepopulated_qr_codes_for_first_user[0]
        updated_title = "Updated QR Code Title"

        update_payload = {"title": updated_title}

        response = await async_client.put(
            f"/api/v1/qr-codes/{qr_code.id}",
            headers={"Authorization": f"Bearer {tokens.access_token}"},
            json=update_payload,
        )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["updatedItem"]["title"] == updated_title

        # Ensure that the title was updated in the database
        await async_db.refresh(qr_code)
        assert qr_code.title == updated_title

    @pytest.mark.asyncio
    async def test_update_qr_code_customization(
            self, async_client: AsyncClient, async_db: AsyncSession,
            tokens: AuthTokens, prepopulated_qr_codes_for_first_user: List[QRCode],
    ):
        """
        Ensures that the customization of the first prepopulated QR code is successfully updated.
        """
        qr_code = prepopulated_qr_codes_for_first_user[0]
        updated_customization = {
            "color": "blue",
            "size": 300,
            "useImage": True
        }

        update_payload = {
            "customization": updated_customization
        }

        response = await async_client.put(
            f"/api/v1/qr-codes/{qr_code.id}",
            headers={"Authorization": f"Bearer {tokens.access_token}"},
            json=update_payload,
        )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["updatedItem"]["customization"] == updated_customization

        # Ensure that the customization was updated in the database
        await async_db.refresh(qr_code)
        assert qr_code.customization == updated_customization

    @pytest.mark.asyncio
    async def test_update_qr_code_only_title(
            self, async_client: AsyncClient, async_db: AsyncSession,
            tokens: AuthTokens, prepopulated_qr_codes_for_first_user: List[QRCode],
    ):
        """
        Ensures that if both title and customization are specified in the update request,
        only the title is updated while the customization remains unchanged.
        """
        qr_code = prepopulated_qr_codes_for_first_user[0]
        original_customization = qr_code.customization  # Store the original customization

        update_payload = {
            "title": "Updated QR Code Title",
            "customization": {
                "color": "red",
                "size": 500
            }
        }

        response = await async_client.put(
            f"/api/v1/qr-codes/{qr_code.id}",
            headers={"Authorization": f"Bearer {tokens.access_token}"},
            json=update_payload,
        )

        assert response.status_code == 200
        response_data = response.json()

        # Ensure only title is updated
        assert response_data["updatedItem"]["title"] == update_payload["title"]
        assert response_data["updatedItem"]["customization"] == original_customization

        # Ensure that only the title was updated in the database
        await async_db.refresh(qr_code)
        assert qr_code.title == update_payload["title"]
        assert qr_code.customization == original_customization  # Customization should remain unchanged

    @pytest.mark.asyncio
    async def test_update_non_existing_qr_code(
            self, async_client: AsyncClient, tokens: AuthTokens
    ):
        """
        Ensures that trying to update a non-existing QR code returns a HTTP 404 status code.
        """
        non_existing_qr_code_id = 9999
        update_payload = {
            "title": "Updated Title",
        }

        response = await async_client.put(
            f"/api/v1/qr-codes/{non_existing_qr_code_id}",
            headers={"Authorization": f"Bearer {tokens.access_token}"},
            json=update_payload,
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_qr_code_not_owner(
            self, async_client: AsyncClient, async_db: AsyncSession,
            tokens: AuthTokens, prepopulated_qr_codes_for_second_user: List[QRCode]
    ):
        """
        Ensures that if the user is not the owner of the QR code, they cannot update it
        and will receive a 403 Forbidden status code.
        """
        qr_code = prepopulated_qr_codes_for_second_user[0]

        # Attempt to update the QR code as a different user (not the owner)
        update_payload = {
            "title": "Unauthorized Update",
        }

        response = await async_client.put(
            f"/api/v1/qr-codes/{qr_code.id}",
            headers={"Authorization": f"Bearer {tokens.access_token}"},
            json=update_payload,
        )

        # Ensure that the response status code is 403 Forbidden
        assert response.status_code == 403
