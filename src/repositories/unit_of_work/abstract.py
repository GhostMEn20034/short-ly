from abc import ABC, abstractmethod


class AbstractUnitOfWork(ABC):
    @abstractmethod
    async def start(self) -> None:
        pass

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
