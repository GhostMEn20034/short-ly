import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import User
from src.schemes.auth.token_data import RefreshTokenRequest, AuthTokens


class TestJWTAuth:

    @pytest.mark.asyncio
    async def test_login_success(self, async_client: AsyncClient, user: User,
                                 async_db: AsyncSession, test_user_password: str):

        # Prepare the login payload
        login_data = {
            "username": user.email,
            "password": test_user_password,
        }
        # # Perform the login request
        response = await async_client.post("/api/v1/auth/token", data=login_data)

        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

    @pytest.mark.asyncio
    async def test_login_incorrect_email(self, async_client: AsyncClient, async_db: AsyncSession):
        # Prepare the login payload with incorrect email
        login_data = {
            "username": "wrong@example.com",
            "password": "some_pwd",
        }

        # Perform the login request
        response = await async_client.post("/api/v1/auth/token", data=login_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert data["detail"][0]["ctx"]["reason"] == "Incorrect email or password"

    @pytest.mark.asyncio
    async def test_login_incorrect_password(self, async_client: AsyncClient, user: User, async_db: AsyncSession):
        # Prepare the login payload with incorrect password
        login_data = {
            "username": user.email,
            "password": "wrong_password",
        }

        # Perform the login request
        response = await async_client.post("/api/v1/auth/token", data=login_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert data["detail"][0]["ctx"]["reason"] == "Incorrect email or password"

    @pytest.mark.asyncio
    async def test_refresh_token_success(self, async_client: AsyncClient, async_db: AsyncSession, tokens: AuthTokens):

        # Prepare the refresh token request
        refresh_token_data = RefreshTokenRequest(refresh_token=tokens.refresh_token)

        # Perform the refresh token request
        response = await async_client.post("/api/v1/auth/token/refresh", json=refresh_token_data.model_dump())

        assert response.status_code == status.HTTP_200_OK
        # Parse response JSON
        response_data = response.json()

        # Assert the keys and their types
        assert "access_token" in response_data
        assert "refresh_token" in response_data
        assert isinstance(response_data["access_token"], str)
        assert isinstance(response_data["refresh_token"], str)


    @pytest.mark.asyncio
    async def test_refresh_token_invalid(self, async_client: AsyncClient, async_db: AsyncSession):
        # Prepare the refresh token request with invalid token
        refresh_token_data = RefreshTokenRequest(refresh_token="invalid_token")

        # Perform the refresh token request
        response = await async_client.post("/api/v1/auth/token/refresh", json=refresh_token_data.model_dump())

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["detail"] == "Could not validate credentials"