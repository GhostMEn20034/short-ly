from typing import List, Optional
from pydantic import BaseModel, Field

from src.schemes.pagination import PaginationResponse
from src.schemes.shortened_url.base import BaseShortenedUrlModel
from src.schemes.qr_code.base import BaseQRCodeSchema

class ShortenedUrlListItem(BaseShortenedUrlModel):
    qr_code_id: int | None = None


class ShortenedUrlDetailsResponseSchema(BaseModel):
    item: BaseShortenedUrlModel
    qr_code: Optional[BaseQRCodeSchema] = Field(None, alias='qrCode')

    class Config:
        populate_by_name = True


class ShortenedUrlListResponseSchema(BaseModel):
    items: List[ShortenedUrlListItem]
    pagination: PaginationResponse
