from abc import abstractmethod, ABC
from typing import Optional, Sequence, Tuple

from src.models.qr_code import QRCode
from src.models.shortened_url import ShortenedUrl
from src.repositories.base.abstract import AbstractGenericRepository
from src.schemes.common import DatetimeRange
from src.schemes.pagination import PaginationParams


class AbstractURLRepositorySQL(AbstractGenericRepository[ShortenedUrl], ABC):

    @abstractmethod
    async def get_by_short_code(self, short_code: str) -> Optional[ShortenedUrl]:
        """
        :param short_code: URL's short code
        :return: ShortenedUrl object if exists
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_by_short_code_with_joined_qr_code(self, short_code: str) -> Tuple[
        Optional[ShortenedUrl], Optional[QRCode]
    ]:
        """
        :param short_code: URL's short code.
        :return: ShortenedUrl and QRCode objects if exist
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_paginated_url_list(self, user_id: int, datetime_range: DatetimeRange,
                                     pagination_params: PaginationParams) -> Tuple[Sequence[ShortenedUrl], int]:
        """
        :param user_id: The owner of shortened urls
        :param datetime_range: Datetime range in which results should be returned
        :param pagination_params: Pagination params like current page, items per page, etc.
        :return: Matched shortened urls (Paginated not the whole matched dataset) and total number of items
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_paginated_url_list_with_qr(
            self, user_id: int, datetime_range: DatetimeRange, pagination_params: PaginationParams
    ) -> Tuple[Sequence[Tuple[ShortenedUrl, Optional[int]]], int]:
        """
        Does the exact same thing as get_paginated_url_list.
        BUT it returns sequence of tuples of shortened url and qr code id (Can be None).
        And it returns total number of items (As usually)
        """
        raise NotImplementedError()

    @abstractmethod
    async def is_shortened_url_exist(self, short_code: str) -> bool:
        raise NotImplementedError()
