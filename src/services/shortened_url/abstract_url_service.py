from abc import ABC, abstractmethod
from typing import Optional, Sequence, Tuple
from pydantic import HttpUrl

from src.models.qr_code import QRCode
from src.models.user import User
from src.models.shortened_url import ShortenedUrl
from src.schemes.common import DatetimeRange
from src.schemes.shortened_url.request_bodies.update import UpdateShortenedUrlSchema
from src.schemes.shortened_url.request_bodies.create import CreateShortenedUrlRequestBody

from src.schemes.pagination import PaginationParams, PaginationResponse
from src.schemes.shortened_url.response_bodies.retrieve import ShortenedUrlListItem


class AbstractURLService(ABC):

    @abstractmethod
    async def create_shortened_url(self, data: CreateShortenedUrlRequestBody, owner: User) -> ShortenedUrl:
        pass


    @abstractmethod
    async def get_shortened_url_list(self, user: User, datetime_range: DatetimeRange,
                                     pagination_params: PaginationParams) \
            -> Tuple[Sequence[ShortenedUrlListItem], PaginationResponse]:
        pass

    @abstractmethod
    async def get_shortened_url_details(self, short_code: str, owner: User) -> Tuple[ShortenedUrl, Optional[QRCode]]:
        pass

    @abstractmethod
    async def get_long_url(self, short_code: str) -> HttpUrl:
        pass

    @abstractmethod
    async def update_shortened_url(self, short_code: str, data: UpdateShortenedUrlSchema, owner: User) -> ShortenedUrl:
        pass

    @abstractmethod
    async def delete_shortened_url(self, short_code: str, owner: User) -> bool:
        pass
