import pytest
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import User
from src.utils.password_utils import hash_password

class TestSignup:
    @pytest.mark.asyncio
    async def test_signup_default_case(self, async_client: AsyncClient, async_db: AsyncSession) -> None:
        response = await async_client.post(
            "/api/v1/users/signup",
            json={
                "email": "newuser@test.com",
                "first_name": "Jane",
                "last_name": "Doe",
                "date_of_birth": "1990-01-01",
                "password1": "password123",
                "password2": "password123"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@test.com"
        assert data["first_name"] == "Jane"
        assert data["last_name"] == "Doe"

        stmt = select(User).where(User.email == "newuser@test.com")
        result = await async_db.exec(stmt)

        assert result.first().email == "newuser@test.com"

    @pytest.mark.asyncio
    async def test_signup_existing_email(self, async_client: AsyncClient, async_db: AsyncSession ):
        # Create user
        user = User(
            email="newuser@test.com",
            first_name="Another",
            last_name="User",
            password1=hash_password("123456tt"),
        )
        async_db.add(user)
        await async_db.commit()

        # Attempt to sign up with the same email as `the_user`
        response = await async_client.post(
            "/api/v1/users/signup",
            json={
                "email": user.email,  # Using the existing user's email
                "first_name": "Another",
                "last_name": "User",
                "date_of_birth": "1995-05-15",
                "password1": "newpassword123",
                "password2": "newpassword123"
            }
        )
        assert response.status_code == 400
        data = response.json()
        assert data["detail"][0]["ctx"]["reason"] == "The user with this email already exists"

    @pytest.mark.asyncio
    async def test_signup_two_passwords_are_different(self, async_client: AsyncClient, async_db: AsyncSession) -> None:
        """
        If password1 and password2 are different, There should be error HTTP 400.
        """
        response = await async_client.post(
            "/api/v1/users/signup",
            json={
                "email": "newuser@test.com",
                "first_name": "Jane",
                "last_name": "Doe",
                "date_of_birth": "1990-01-01",
                "password1": "password123",
                "password2": "password1234"
            }
        )
        assert response.status_code == 422