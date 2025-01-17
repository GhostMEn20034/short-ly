from typing import Any
from sqlmodel.ext.asyncio.session import AsyncSession

from .abstract import AbstractUnitOfWork
from src.repositories.user.abstract import AbstractUserRepository
from src.repositories.shortened_url.abstract import AbstractURLRepositorySQL


class UnitOfWork(AbstractUnitOfWork):

    def __init__(self, session: AsyncSession,
                 user_repository: AbstractUserRepository,
                 url_repository: AbstractURLRepositorySQL
                 ):
        self._session = session
        self.user_repository = user_repository
        self.url_repository = url_repository

    async def commit(self) -> None:
        """Saves all changes to the database."""
        await self._session.commit()

    async def close(self) -> None:
        """Closes the session."""
        await self._session.close()

    async def rollback(self) -> None:
        """Rollback the current transaction."""
        await self._session.rollback()

    async def __aenter__(self) -> "UnitOfWork":
        """Allows the use of 'async with' to manage resources."""
        return self

    async def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Handles the exit of the context manager."""
        if exc_type is not None:
            await self.rollback()  # Rollback if an exception occurred

        await self.close()  # Ensure the session is closed