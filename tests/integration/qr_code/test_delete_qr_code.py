import pytest
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.models.qr_code import QRCode
from src.schemes.auth.token_data import AuthTokens
from typing import List

class TestDeleteQRCode:

    @pytest.mark.asyncio
    async def test_delete_qr_code_successfully(
            self, async_client: AsyncClient, async_db: AsyncSession,
            tokens: AuthTokens, prepopulated_urls: List[QRCode], prepopulated_qr_codes_for_first_user,
    ):
        """
        Ensures that the QR code is deleted successfully, and there is no QR code associated with the provided link_id.
        """

        link_id = prepopulated_qr_codes_for_first_user[0].id

        # Check if the QR code exists for the given link_id before deleting
        qr_code_before_delete = await async_db.exec(
            select(QRCode).where(QRCode.link_id == link_id)
        )
        qr_code_before_delete = qr_code_before_delete.first()

        # Assert that there is a QR code linked to the link_id before deleting
        assert qr_code_before_delete is not None

        # Send DELETE request to delete the QR code associated with the given short code
        response = await async_client.delete(
            f"/api/v1/urls/{prepopulated_urls[0].short_code}",
            headers={"Authorization": f"Bearer {tokens.access_token}"}
        )

        # Assert the response status code is 204 No Content (successfully deleted)
        assert response.status_code == 204

        # Query the database to check if the QR code with the link_id of the deleted URL exists
        qr_code_after_delete = await async_db.exec(
            select(QRCode).where(QRCode.link_id == link_id)
        )
        qr_code_after_delete = qr_code_after_delete.first()

        # Assert that no QR code exists for the given link_id after deletion
        assert qr_code_after_delete is None
