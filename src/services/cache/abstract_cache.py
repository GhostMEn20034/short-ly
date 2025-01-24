from abc import ABC, abstractmethod
from typing import Optional, Dict


class AbstractCacheService(ABC):
    """
    Abstract base class that defines the interface for all cached services.
    """
    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_object(self, key: str) -> Optional[Dict]:
        pass

    @abstractmethod
    async def set_object(self, key: str, value: Dict, ttl: Optional[int] = None) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        raise NotImplementedError
