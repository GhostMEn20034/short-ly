import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import User
from src.schemes.auth.token_data import AuthTokens
from src.utils.password_utils import hash_password


class TestChangeEmail:

    @pytest.mark.asyncio
    async def test_change_email_default_case(
            self, async_client: AsyncClient, tokens: AuthTokens,
    ):
        response = await async_client.put(
            "/api/v1/users/change-email",
            json={
                "email": "user20004@example.com",
            },
            headers={"Authorization": f"Bearer {tokens.access_token}"}
        )
        assert response.status_code == 200


    @pytest.mark.asyncio
    async def test_update_user_with_existing_email(self, async_client: AsyncClient, async_db: AsyncSession,
                                                   tokens: AuthTokens):
        another_user = User(
            email="anotheremail@test.com",
            first_name="John",
            last_name="Doe",
            password=hash_password("123sdxsff")
        )

        async_db.add(another_user)
        await async_db.flush()
        await async_db.commit()

        # Try updating `the_user` to use `another_user`'s email
        response = await async_client.put(
            "/api/v1/users/change-email",
            json={
                "email": another_user.email,  # Attempting to use the existing user's email
            },
            headers={"Authorization": f"Bearer {tokens.access_token}"}
        )
        assert response.status_code == 400
        data = response.json()
        assert data["detail"][0]["ctx"]["reason"] == "The user with this email already exists"
