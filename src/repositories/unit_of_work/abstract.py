from abc import ABC, abstractmethod

from src.repositories.shortened_url.abstract import AbstractURLRepositorySQL
from src.repositories.user.abstract import AbstractUserRepository


class AbstractUnitOfWork(ABC):
    user_repository: AbstractUserRepository
    url_repository: AbstractURLRepositorySQL

    @abstractmethod
    async def commit(self) -> None:
        """Saves all changes to the database."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Closes the session."""
        pass

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the current transaction."""
        pass
