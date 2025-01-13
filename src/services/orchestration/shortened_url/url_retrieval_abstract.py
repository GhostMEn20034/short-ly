from abc import ABC, abstractmethod


class AbstractUrlRetrievalOrchestrator(ABC):
    """
    Class responsible to orchestrate/coordinate services classes to retrieve full url using short code.
    """
    @abstractmethod
    async def retrieve_url(self, short_code: str) -> str:
        raise NotImplementedError
