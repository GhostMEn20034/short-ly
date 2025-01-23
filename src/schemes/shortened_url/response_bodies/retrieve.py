from typing import List
from pydantic import BaseModel

from src.schemes.pagination import PaginationResponse
from src.schemes.shortened_url.base import BaseShortenedUrlModel


class ShortenedUrlDetailsResponseSchema(BaseModel):
    item: BaseShortenedUrlModel


class ShortenedUrlListResponseSchema(BaseModel):
    items: List[BaseShortenedUrlModel]
    pagination: PaginationResponse
