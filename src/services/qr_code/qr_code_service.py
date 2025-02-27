from fastapi import HTTPException, status

from .abstract_qr_code_service import AbstractQRCodeService
from src.models.user import User
from src.models.qr_code import QRCode
from src.models.shortened_url import ShortenedUrl
from src.schemes.qr_code.request_bodies.create import CreateQRCodeSchema
from src.repositories.unit_of_work.abstract import AbstractUnitOfWork
from src.repositories.qr_code.abstract import AbstractQRCodeRepository
from src.utils.error_utils import generate_error_response


class QRCodeService(AbstractQRCodeService):
    def __init__(self,
                 uow: AbstractUnitOfWork,
                 qr_code_repository: AbstractQRCodeRepository,
                 ):
        self._uow = uow
        self._qr_code_repository = qr_code_repository

    async def create_qr_code(self, qr_code_payload: CreateQRCodeSchema, link: ShortenedUrl, user_id: int) -> QRCode:
        # Check if a QR code with the same link_id already exists
        existing_qr_code = await self._qr_code_repository.get_by_link_id(link.id)
        if existing_qr_code:
            error_details = generate_error_response(
                location=["body", "linkShortCode"],
                message="Cannot create a QR Code",
                reason="There's already a QR code for the link with the given short code.",
                input_value=link.short_code,
                error_type="domain_error"
            )

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=[error_details])

        # Create and insert a new QR code
        qr_code_to_create = QRCode(
            title=link.friendly_name,
            image=str(qr_code_payload.image) if qr_code_payload.image is not None else None,
            customization=qr_code_payload.customization,
            user_id=user_id,
            link_id=link.id,
        )
        qr_code_to_create = await self._qr_code_repository.add(qr_code_to_create)
        await self._uow.commit()

        return qr_code_to_create

    async def get_qr_code_with_link(self, qr_code_id: int, user: User) -> QRCode:
        """
        :param qr_code_id: The ID of the QR code the user want to retrieve.
        :param user: The user whose QR code is to be retrieved.
        :return: QR code and related link
        """
        qr_code = await self._qr_code_repository.get_by_id_with_joined_link(qr_code_id)

        if not qr_code:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if user.id != qr_code.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not the owner of this QR Code"
            )

        return qr_code

