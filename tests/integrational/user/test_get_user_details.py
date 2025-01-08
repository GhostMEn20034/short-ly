import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.user import User
from src.schemes.auth.token_data import AuthTokens


class TestGetUserDetails:

    @pytest.mark.asyncio
    async def test_get_user_details(self, async_client: AsyncClient, async_db: AsyncSession, user: User, tokens: AuthTokens):

        response = await async_client.get("/api/v1/users/details",
                                          headers={"Authorization": f"Bearer {tokens.access_token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user.email
        assert data["first_name"] == user.first_name
