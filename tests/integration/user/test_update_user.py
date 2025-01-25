import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import User
from src.schemes.auth.token_data import AuthTokens


class TestUserUpdate:
    @pytest.mark.asyncio
    async def test_update_user(self, async_client: AsyncClient, async_db: AsyncSession, user: User, tokens: AuthTokens):
        response = await async_client.put(
            "/api/v1/users/update",
            json={
                "first_name": "John",
                "last_name": "Doe",
            },
            headers={"Authorization": f"Bearer {tokens.access_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "John"

    @pytest.mark.asyncio
    async def test_update_user_with_last_name_none(
            self, async_client: AsyncClient, async_db: AsyncSession,
            user: User, tokens: AuthTokens,
    ):
        """
        If user does not specify last name, everything still should be fine ( HTTP 200 OK )
        """
        response = await async_client.put(
            "/api/v1/users/update",
            json={
                "first_name": "John",
            },
            headers={"Authorization": f"Bearer {tokens.access_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "John"
        assert data["last_name"] is None
