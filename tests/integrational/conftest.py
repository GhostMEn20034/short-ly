import asyncio
import os
import pytest
from typing import AsyncGenerator
from dependency_injector import providers
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.app_factory import create_app
from src.models import User
from src.utils.password_utils import hash_password
from src.schemes.auth.token_data import AuthTokens
from src.services.cache.cache_stub import CacheServiceStub


engine = create_async_engine(os.getenv("DB_CONNECTION_STRING"), echo=True, poolclass=NullPool)

@pytest.fixture(scope="session")
async def async_db_engine():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope="function")
async def async_db(async_db_engine):
    """
    Async database session
    """
    async_session = sessionmaker(
        bind=async_db_engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        class_=AsyncSession,
    )

    async with async_session() as session:
        try:
            await session.begin()
            yield session
        finally:
            await session.close_all()
            for table in reversed(SQLModel.metadata.sorted_tables):
                await session.exec(text(f'TRUNCATE "{table.name}" CASCADE;'))
                await session.exec(
                    text(f"ALTER SEQUENCE {table.name}_id_seq RESTART WITH 1;")
                )
            await session.commit()


@pytest.fixture(scope="session")
async def app() -> FastAPI:
    return create_app()


@pytest.fixture(scope="session")
async def async_client(app) -> AsyncGenerator[AsyncClient, None]:
    app.container.redis_cache_service.override(providers.Singleton(CacheServiceStub))

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
         ) as ac:
        yield ac


# let test session to know it is running inside event loop
@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

# ↓ For Providing test data ↓

@pytest.fixture(scope='session')
async def test_user_password() -> str:
    return "123456tt"

@pytest.fixture(scope="function")
async def user(async_db, test_user_password) -> User:
    user = User(
        email="newuser@test.com",
        first_name="John",
        last_name="Doe",
        password=hash_password(test_user_password),
    )

    async_db.add(user)
    await async_db.commit()

    return user

@pytest.fixture(scope="function")
async def tokens(user, async_db, async_client, test_user_password) -> AuthTokens:
    # Prepare the login payload
    login_data = {
        "username": user.email,
        "password": test_user_password,
    }
    # Perform the login request
    response = await async_client.post("/api/v1/auth/token", data=login_data)

    data = response.json()
    return AuthTokens(**data)
