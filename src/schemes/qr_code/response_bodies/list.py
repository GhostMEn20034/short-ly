from typing import List
from pydantic import BaseModel

from src.schemes.pagination import PaginationResponse
from .details import QRCodeDetailsResponse


class QRCodeListResponse(BaseModel):
    items: List[QRCodeDetailsResponse]
    pagination: PaginationResponse
