from abc import ABC, abstractmethod
from typing import Optional, Sequence, Tuple

from src.models import User
from src.models.qr_code import QRCode
from src.repositories.base.abstract import AbstractGenericRepository
from src.schemes.common import DatetimeRange
from src.schemes.pagination import PaginationParams


class AbstractQRCodeRepository(AbstractGenericRepository[QRCode], ABC):

    @abstractmethod
    async def get_by_link_id(self, link_id: int) -> Optional[QRCode]:
        """
        Get a single QR Code by the link id.

        :param link_id: (int): Link id (Foreign key).
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id_with_joined_link(self, qr_code_id: int) -> Optional[QRCode]:
        """
        Get a single QR Code with the joined link. primary key used as a filter.
        :param qr_code_id:
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_paginated_list_of_qr_codes_with_joined_links(
            self, user: User, datetime_range: DatetimeRange, pagination_params: PaginationParams) -> Tuple[Sequence[QRCode], int]:
        """
        :param user: QR codes' owner.
        :param datetime_range: Datetime range over which to retrieve QR codes.
        :param pagination_params: pagination parameters (page size, page number, etc.)
        :return: Sequence of user's QR Codes and total pages count
        """
        raise NotImplementedError()
