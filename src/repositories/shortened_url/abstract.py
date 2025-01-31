from abc import abstractmethod, ABC
from typing import Optional, List, Sequence, Tuple

from src.models.shortened_url import ShortenedUrl
from src.repositories.base.abstract import AbstractGenericRepository
from src.schemes.common import DatetimeRange
from src.schemes.pagination import PaginationParams


class AbstractURLRepositorySQL(AbstractGenericRepository[ShortenedUrl], ABC):

    @abstractmethod
    async def get_by_short_code(self, short_code: str) -> Optional[ShortenedUrl]:
        raise NotImplementedError()

    @abstractmethod
    async def get_paginated_url_list(self, user_id: int, datetime_range: DatetimeRange,
                                     pagination_params: PaginationParams) -> Tuple[Sequence[ShortenedUrl], int]:
        raise NotImplementedError()

    @abstractmethod
    async def is_shortened_url_exist(self, short_code: str) -> bool:
        raise NotImplementedError()
