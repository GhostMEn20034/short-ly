from abc import ABC, abstractmethod
from typing import Optional

from src.models.qr_code import QRCode
from src.repositories.base.abstract import AbstractGenericRepository


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
        :return:
        """
        raise NotImplementedError()

