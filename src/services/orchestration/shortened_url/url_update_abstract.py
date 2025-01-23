from abc import ABC, abstractmethod

from src.models import User, ShortenedUrl
from src.schemes.shortened_url.request_bodies.update import UpdateShortenedUrlSchema


class AbstractUrlUpdateOrchestrator(ABC):

    @abstractmethod
    async def update_url(self, short_code: str, data: UpdateShortenedUrlSchema, owner: User) -> ShortenedUrl:
        pass
