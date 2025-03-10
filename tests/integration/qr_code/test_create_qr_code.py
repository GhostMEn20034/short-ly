import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import User
from src.models.qr_code import QRCode
from src.models.shortened_url import ShortenedUrl
from src.schemes.auth.token_data import AuthTokens
from src.schemes.qr_code.request_bodies.create import CreateQRCodeSchema, CreateQRCodeRequestBody
from src.schemes.shortened_url.request_bodies.create import CreateShortenedUrlRequestBody


class TestCreateQRCode:

    @pytest.mark.asyncio
    async def test_create_qr_code_with_new_link_default_case(
            self, async_client: AsyncClient, async_db: AsyncSession, tokens: AuthTokens
    ):
        """
        If the user provides link data and QR code data, this route will create a shortened link
        and a QR code. The QR code will be bound to the created link.
        """
        link = CreateShortenedUrlRequestBody(
            friendly_name="Test link",
            is_short_code_custom=True,
            short_code="test-link",
            long_url="https://test-link.com/profile/ghost1k44",
        )

        qr_code = CreateQRCodeSchema(
            image=None,
            customization={"hello": "world", "useImage": False}
        )

        request_body = CreateQRCodeRequestBody(
            link_to_create=link,
            qr_code=qr_code,
        )
        serialized_body = request_body.model_dump()
        serialized_body["link_to_create"]["long_url"] = str(serialized_body["link_to_create"]["long_url"])
        response = await async_client.post("/api/v1/qr-codes/",
                                           headers={"Authorization": f"Bearer {tokens.access_token}"},
                                           json=serialized_body, )

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()

        assert response_data["createdItem"]["title"] == link.friendly_name

        # Ensure that QRCode and Shortened URL exist after the insertion
        stmt = select(QRCode, ShortenedUrl).where(QRCode.id == response_data["createdItem"]["id"]).join(ShortenedUrl)
        result = await async_db.exec(stmt)
        row = result.first()
        assert row is not None
        if row is not None:
            qr_code, shortened_url = row
            assert shortened_url is not None
            assert qr_code is not None


    @pytest.mark.asyncio
    async def test_create_qr_code_for_existing_link_default_case(
            self, async_client: AsyncClient, async_db: AsyncSession, tokens: AuthTokens, user: User
    ):
        """
        If the short code of a link is specified, this route will create a QR code
        and bind it to the link associated with the given short code.
        """
        new_link = ShortenedUrl(
            friendly_name="Test link",
            is_short_code_custom=True,
            short_code="test-link",
            long_url="https://test-link.com/profile/ghost1k44",
            user_id=user.id,
        )

        async_db.add(new_link)
        await async_db.commit()

        qr_code = CreateQRCodeSchema(
            image=None,
            customization={"hello": "world", "useImage": False}
        )

        request_body = CreateQRCodeRequestBody(
            link_short_code=new_link.short_code,
            qr_code=qr_code,
        )
        serialized_body = request_body.model_dump()
        response = await async_client.post("/api/v1/qr-codes/",
                                           headers={"Authorization": f"Bearer {tokens.access_token}"},
                                           json=serialized_body, )

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["createdItem"]["title"] == new_link.friendly_name

        # Ensure that QRCode exists after the insertion
        stmt = select(QRCode).where(QRCode.id == response_data["createdItem"]["id"])
        result = await async_db.exec(stmt)
        created_qr_code = result.first()
        assert created_qr_code is not None


    @pytest.mark.asyncio
    async def test_create_qr_code_with_both_existing_and_new_link_data(
            self, async_client: AsyncClient, async_db: AsyncSession, tokens: AuthTokens, user: User
    ):
        """
        If both the short code of an existing link and new link data are provided,
        the data required to create a new link will be ignored, and the QR code
        will be bound to the link associated with the specified short code.
        """
        existing_link = ShortenedUrl(
            friendly_name="Existing Test Link",
            is_short_code_custom=True,
            short_code="existing-link",
            long_url="https://test-link.com/existing",
            user_id=user.id,
        )

        async_db.add(existing_link)
        await async_db.commit()

        new_link = CreateShortenedUrlRequestBody(
            friendly_name="New Test Link",
            is_short_code_custom=True,
            short_code="new-test-link",
            long_url="https://test-link.com/new",
        )

        qr_code = CreateQRCodeSchema(
            image=None,
            customization={"hello": "world", "useImage": False}
        )

        request_body = CreateQRCodeRequestBody(
            link_short_code=existing_link.short_code,
            link_to_create=new_link,
            qr_code=qr_code,
        )
        serialized_body = request_body.model_dump()
        serialized_body["link_to_create"]["long_url"] = str(serialized_body["link_to_create"]["long_url"])
        response = await async_client.post("/api/v1/qr-codes/",
                                           headers={"Authorization": f"Bearer {tokens.access_token}"},
                                           json=serialized_body, )

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["createdItem"]["title"] == existing_link.friendly_name

        # Ensure that QRCode is bound to the existing link and that the new link was ignored
        stmt = select(QRCode, ShortenedUrl).where(QRCode.id == response_data["createdItem"]["id"]).join(ShortenedUrl)
        result = await async_db.exec(stmt)
        row = result.first()
        assert row is not None
        if row is not None:
            qr_code, bound_link = row
            assert bound_link.short_code == existing_link.short_code  # Ensure it's bound to the existing link
            assert bound_link.long_url == existing_link.long_url

    @pytest.mark.asyncio
    async def test_create_qr_code_with_non_existing_short_code(
            self, async_client: AsyncClient, async_db: AsyncSession, tokens: AuthTokens
    ):
        """
        If a non-existing short code is provided, the request should fail,
        no QR code should be created, and the response should return HTTP 404.
        """
        non_existing_short_code = "non-existing-link"

        qr_code = CreateQRCodeSchema(
            image=None,
            customization={"hello": "world", "useImage": False}
        )

        request_body = CreateQRCodeRequestBody(
            link_short_code=non_existing_short_code,
            qr_code=qr_code,
        )
        serialized_body = request_body.model_dump()
        response = await async_client.post("/api/v1/qr-codes/",
                                           headers={"Authorization": f"Bearer {tokens.access_token}"},
                                           json=serialized_body, )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_create_qr_code_for_link_user_does_not_own(
            self, async_client: AsyncClient, async_db: AsyncSession, tokens: AuthTokens, second_user: User
    ):
        """
        If a user attempts to create a QR code for a link they do not own,
        the request should be denied with HTTP 403, and no QR code should be created.
        """
        # Create a link that belongs to another user
        other_users_link = ShortenedUrl(
            friendly_name="Other User's Link",
            is_short_code_custom=True,
            short_code="other-user-link",
            long_url="https://test-link.com/profile/otheruser",
            user_id=second_user.id,  # Belongs to a different user
        )

        async_db.add(other_users_link)
        await async_db.commit()

        qr_code = CreateQRCodeSchema(
            image=None,
            customization={"hello": "world", "useImage": False}
        )

        request_body = CreateQRCodeRequestBody(
            link_short_code=other_users_link.short_code,
            qr_code=qr_code,
        )
        serialized_body = request_body.model_dump()
        response = await async_client.post("/api/v1/qr-codes/",
                                           headers={"Authorization": f"Bearer {tokens.access_token}"},
                                           json=serialized_body, )

        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Ensure that no QRCode was created
        stmt = select(QRCode).where(QRCode.link_id == other_users_link.id)
        result = await async_db.exec(stmt)
        created_qr_code = result.first()
        assert created_qr_code is None, ("The user must not be able to create "
                                         "a qr code bound to the link the user does not own")
