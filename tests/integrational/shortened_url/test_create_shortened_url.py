from typing import List
from unittest import mock

import pytest
from fastapi import status, FastAPI
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.exceptions.shortened_url import MaxRetriesExceeded
from src.core.containers import Container
from src.models.shortened_url import ShortenedUrl
from src.schemes.auth.token_data import AuthTokens
from src.schemes.shortened_url import CreateShortenedUrlSchema
from src.services.short_code_generator.implementation import ShortCodeGenerator


class TestCreateShortenedUrl:

    @pytest.mark.asyncio
    async def test_create_url_default_case(self, async_client: AsyncClient, async_db: AsyncSession, tokens: AuthTokens):
        """
        If our user entered data correctly, then the user will get successful result HTTP 201 CREATED
        """
        request_body = CreateShortenedUrlSchema(
            friendly_name="Twitch TV",
            is_short_code_custom=False,
            long_url="https://www.twitch.tv/"
        ) # There's no custom short code, so an api will generate a random one

        serialized_body = request_body.model_dump()
        serialized_body["long_url"] = str(serialized_body["long_url"])

        response = await async_client.post("/api/v1/urls/",
                                           headers={"Authorization": f"Bearer {tokens.access_token}"},
                                           json=serialized_body,
                                           )

        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()

        # Ensure that the record exists after the insertion
        stmt = select(ShortenedUrl).where(ShortenedUrl.id == response_data["id"])
        result = await async_db.exec(stmt)
        create_shortened_url = result.first()
        assert create_shortened_url is not None

        # Ensure that shortened url's short code is generated
        assert create_shortened_url.short_code is not None

    async def test_create_url_with_custom_short_code(self, async_client: AsyncClient, async_db: AsyncSession,
                                                     tokens: AuthTokens):
        """
        If user specified is_short_code_custom=True, then the user will get successful result HTTP 201 CREATED.
        And shortened url will have custom short code.
        """
        request_body = CreateShortenedUrlSchema(
            friendly_name="Twitch TV",
            is_short_code_custom=True,
            short_code="twitch-tv-url",
            long_url="https://www.twitch.tv/"
        ) # There's a custom short code and is_short_code_custom=True,
        # so an api won't generate a random short code

        serialized_body = request_body.model_dump()
        serialized_body["long_url"] = str(serialized_body["long_url"])

        response = await async_client.post("/api/v1/urls/",
                                           headers={"Authorization": f"Bearer {tokens.access_token}"},
                                           json=serialized_body,
                                           )

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()

        # Ensure that the url has custom short code
        stmt = select(ShortenedUrl).where(ShortenedUrl.id == response_data["id"])
        result = await async_db.exec(stmt)
        create_shortened_url = result.first()

        assert create_shortened_url.short_code == request_body.short_code

    @pytest.mark.asyncio
    async def test_create_url_with_provided_short_code_but_is_short_code_custom_false(
            self, async_client: AsyncClient, async_db: AsyncSession, tokens: AuthTokens
    ):
        """
        If the user provides a custom short code but is_short_code_custom is set to False,
        the custom short code will be ignored, and a random short code will be generated by the API.
        """
        request_body = CreateShortenedUrlSchema(
            friendly_name="Twitch TV",
            is_short_code_custom=False,
            short_code="twitch-tv-url",  # Custom short code provided, but will be ignored
            long_url="https://www.twitch.tv/"
        ) # There's a custom short code, but is_short_code_custom=False,
        # so an api will generate a random short code anyway

        serialized_body = request_body.model_dump()
        serialized_body["long_url"] = str(serialized_body["long_url"])

        response = await async_client.post("/api/v1/urls/",
                                           headers={"Authorization": f"Bearer {tokens.access_token}"},
                                           json=serialized_body,
                                           )

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()

        # Ensure that the url's short code is not equal to specified by the user
        stmt = select(ShortenedUrl).where(ShortenedUrl.id == response_data["id"])
        result = await async_db.exec(stmt)
        create_shortened_url = result.first()

        assert create_shortened_url.short_code != request_body.short_code

    @pytest.mark.asyncio
    async def test_create_url_with_existing_short_code(
            self, async_client: AsyncClient, async_db: AsyncSession, prepopulated_urls: List[ShortenedUrl],
            tokens: AuthTokens,
    ):
        """
        If the user decided to use custom short code and this short code already exists,
        then the user will get HTTP 400 BAD REQUEST error
        """
        request_body = CreateShortenedUrlSchema(
            friendly_name="Twitch TV",
            is_short_code_custom=True,
            short_code=prepopulated_urls[0].short_code,
            long_url="https://www.twitch.tv/"
        )

        serialized_body = request_body.model_dump()
        serialized_body["long_url"] = str(serialized_body["long_url"])

        response = await async_client.post("/api/v1/urls/",
                                           headers={"Authorization": f"Bearer {tokens.access_token}"},
                                           json=serialized_body,
                                           )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_create_url_server_cannot_generate_short_code(
            self, app: FastAPI, async_client: AsyncClient, async_db: AsyncSession,
            tokens: AuthTokens,
    ):
        """
        If a server cannot generate short code, then the server return HTTP 500 INTERNAL SERVER ERROR
        """
        code_generator_mock = mock.AsyncMock(spec=ShortCodeGenerator)
        code_generator_mock.generate_short_code.side_effect = MaxRetriesExceeded(5)

        request_body = CreateShortenedUrlSchema(
            friendly_name="Some URL",
            is_short_code_custom=False,
            long_url="https://www.twitch.tv/"
        )

        serialized_body = request_body.model_dump()
        serialized_body["long_url"] = str(serialized_body["long_url"])

        container: Container = app.container

        with container.short_code_generator.override(code_generator_mock):
            response = await async_client.post("/api/v1/urls/",
                                           headers={"Authorization": f"Bearer {tokens.access_token}"},
                                           json=serialized_body,
                                           )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
