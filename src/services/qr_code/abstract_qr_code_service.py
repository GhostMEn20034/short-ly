from abc import ABC, abstractmethod
from typing import Sequence, Tuple

from src.models.user import User
from src.models.shortened_url import ShortenedUrl
from src.models.qr_code import QRCode
from src.schemes.pagination import PaginationParams, PaginationResponse
from src.schemes.qr_code.request_bodies.create import CreateQRCodeSchema
from src.schemes.qr_code.request_bodies.update import UpdateQRCode, UpdateQRCodeCustomization


class AbstractQRCodeService(ABC):

    @abstractmethod
    async def create_qr_code(self, qr_code_payload: CreateQRCodeSchema, link: ShortenedUrl, user_id: int) -> QRCode:
        """
        :param qr_code_payload: The schema containing QR code details, such as title, image, and customization options.
        :param link: The shortened link associated with the QR code.
        :param user_id: The ID of the owner of the QR code that will be created.
        :return: created QR code.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_qr_codes_with_links(self, user: User, pagination_params: PaginationParams)  \
                                                                         -> Tuple[Sequence[QRCode], PaginationResponse]:
        """
        :param user: The user who wants to retrieve his QR codes.
        :param pagination_params: pagination parameters (page size, page number, etc.)
        :return: Sequence of user's QR Codes
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_qr_code_with_link(self, qr_code_id: int, user: User) -> QRCode:
        """
        :param qr_code_id: The ID of the QR code the user want to retrieve.
        :param user: The user whose QR code is to be retrieved.
        :return: QR code and related link
        """
        raise NotImplementedError()

    @abstractmethod
    async def update_qr_code(self, qr_code_id: int, user: User,
                             data_to_update: UpdateQRCode | UpdateQRCodeCustomization) -> QRCode:
        """
        :param user: The user who wants to update the QR code ( Must be owner ).
        :param qr_code_id: Identifier of the QR code to be updated.
        :param data_to_update: Data need to be applied to the QR code.
        :return: Updated QR code.
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete_qr_code(self, qr_code_id: int, user: User) -> None:
        """
        :param qr_code_id: Identifier of the QR code to be deleted.
        :param user: The user who wants to delete the QR code ( Must be owner )
        :return: Nothing, Because there's no qr code already
        """
        raise NotImplementedError()
