from typing import Any
from sqlmodel.ext.asyncio.session import AsyncSession

from .abstract import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    """
    This class manages a transactional unit of work within a database session.

    Fields:
    `session` is an instance of `AsyncSession` that manages the database transaction.
                        This session is used to interact with the database within the transaction
                        boundary. It is required to begin, commit, rollback, and close the session.

    `_should_commit` flag controls whether or not changes in the transaction
    are committed to the database. By default, it is set to `True`, meaning that
    commit operations are allowed. If the flag is set to `False` using the
    `prevent_commit` method, the commit operation will be skipped when the
    `commit()` method is called, allowing for more flexibility in certain scenarios.

    Why It’s Useful:
    - This approach is helpful when you need to perform multiple database operations as part of a
      transaction, but you want to delay the commit until certain conditions are met, or if an
      operation fails, so you can prevent the commit during error handling or conditional logic.
    """

    def __init__(self, session: AsyncSession,
                 ):
        self._session = session
        self._should_commit = True

    async def start(self):
        await self._session.begin()

    async def commit(self) -> None:
        """Saves all changes to the database."""
        if self._should_commit:
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

    def prevent_commit(self):
        """
        After calling this method, all commit operations will be ignored.
        """
        self._should_commit = False

    def allow_commit(self):
        """
        To allow commit operations, you need to call this method
        """
        self._should_commit = True
