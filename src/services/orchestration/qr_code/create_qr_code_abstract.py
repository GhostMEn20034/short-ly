from abc import ABC, abstractmethod

from src.models.user import User
from src.models.qr_code import QRCode
from src.schemes.qr_code.request_bodies.create import CreateQRCodeRequestBody


class AbstractQRCodeCreationOrchestrator(ABC):

    @abstractmethod
    async def create_qr_code(self, create_qr_code_payload: CreateQRCodeRequestBody, creator: User) -> QRCode:
        pass
