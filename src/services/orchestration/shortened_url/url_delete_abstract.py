from abc import ABC, abstractmethod

from src.models import User


class AbstractUrlDeleteOrchestrator(ABC):
    @abstractmethod
    async def delete_url(self, short_code: str, owner: User):
        pass