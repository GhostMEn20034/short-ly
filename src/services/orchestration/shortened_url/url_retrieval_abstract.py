from abc import ABC, abstractmethod
from typing import Tuple


class AbstractUrlRetrievalOrchestrator(ABC):
    """
    Class responsible to orchestrate/coordinate services classes to retrieve full url using short code.
    """
    @abstractmethod
    async def retrieve_url(self, short_code: str) -> Tuple[str, str]:
        raise NotImplementedError
