from abc import ABC, abstractmethod

from src.models.user import User
from src.models.shortened_url import ShortenedUrl
from src.models.qr_code import QRCode
from src.schemes.qr_code.request_bodies.create import CreateQRCodeSchema


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
    async def get_qr_code_with_link(self, qr_code_id: int, user: User) -> QRCode:
        """
        :param qr_code_id: The ID of the QR code the user want to retrieve.
        :param user: The user whose QR code is to be retrieved.
        :return: QR code and related link
        """
        raise NotImplementedError()
