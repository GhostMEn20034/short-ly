from abc import abstractmethod, ABC
from typing import Optional

from src.models.shortened_url import ShortenedUrl
from src.repositories.base.abstract_sql import AbstractGenericRepository


class AbstractURLRepositorySQL(AbstractGenericRepository[ShortenedUrl], ABC):

    @abstractmethod
    async def get_by_short_code(self, short_code: str) -> Optional[ShortenedUrl]:
        raise NotImplementedError()

    @abstractmethod
    async def is_shortened_url_exist(self, short_code: str) -> bool:
        raise NotImplementedError()
