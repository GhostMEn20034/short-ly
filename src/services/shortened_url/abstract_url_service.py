from abc import ABC, abstractmethod
from typing import Optional, List
from pydantic import HttpUrl

from src.models.user import User
from src.models.shortened_url import ShortenedUrl
from src.schemes.shortened_url import CreateShortenedUrlSchema, UpdateShortenedUrlSchema


class AbstractURLService(ABC):

    @abstractmethod
    async def create_shortened_url(self, data: CreateShortenedUrlSchema, owner: User) -> ShortenedUrl:
        pass


    @abstractmethod
    async def get_shortened_url_list(self, user: User) -> List[ShortenedUrl]:
        pass

    @abstractmethod
    async def get_shortened_url_details(self, short_code: str, owner: User) -> Optional[ShortenedUrl]:
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
