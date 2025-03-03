from typing import Sequence, Tuple
from fastapi import HTTPException, status

from .abstract_qr_code_service import AbstractQRCodeService
from src.models.user import User
from src.models.qr_code import QRCode
from src.models.shortened_url import ShortenedUrl
from src.schemes.pagination import PaginationParams, PaginationResponse
from src.schemes.qr_code.request_bodies.create import CreateQRCodeSchema
from src.schemes.qr_code.request_bodies.update import UpdateQRCode, UpdateQRCodeCustomization
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

    async def get_qr_codes_with_links(self, user: User, pagination_params: PaginationParams) \
            -> Tuple[Sequence[QRCode], PaginationResponse]:
        qr_codes, total_count = await self._qr_code_repository.get_paginated_list_of_qr_codes_with_joined_links(
            user,
            pagination_params,
        )

        total_pages = pagination_params.get_total_pages(total_count)

        pagination_response = PaginationResponse(
            current_page=pagination_params.page,
            page_size=pagination_params.page_size,
            total_pages=total_pages,
            total_items=total_count,
        )

        return qr_codes, pagination_response

    async def get_qr_code_with_link(self, qr_code_id: int, user: User) -> QRCode:
        qr_code = await self._qr_code_repository.get_by_id_with_joined_link(qr_code_id)

        if not qr_code:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if user.id != qr_code.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not the owner of this QR Code"
            )

        return qr_code

    async def update_qr_code(self, qr_code_id: int, user: User,
                             data_to_update: UpdateQRCode | UpdateQRCodeCustomization) -> QRCode:
        qr_code = await self._qr_code_repository.get_by_id(qr_code_id)
        if not qr_code:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if user.id != qr_code.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not the owner of this QR Code"
            )

        self.__apply_changes_to_qr_code(qr_code, data_to_update)
        updated_qr_code = await self._qr_code_repository.update(qr_code)
        await self._uow.commit()

        return updated_qr_code

    async def delete_qr_code(self, qr_code_id: int, user: User) -> None:
        qr_code = await self._qr_code_repository.get_by_id(qr_code_id)
        if not qr_code:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if user.id != qr_code.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not the owner of this QR Code"
            )

        await self._qr_code_repository.delete(qr_code)
        await self._uow.commit()

    # Utility methods --------------------------------------------------------------------------------------------------

    @staticmethod
    def __apply_changes_to_qr_code(qr_code: QRCode,
                                   data_to_update: UpdateQRCode | UpdateQRCodeCustomization):
        if isinstance(data_to_update, UpdateQRCode):
            qr_code.title = data_to_update.title
        elif isinstance(data_to_update, UpdateQRCodeCustomization):
            qr_code.image = str(data_to_update.image) if data_to_update.image is not None else None
            qr_code.customization = data_to_update.customization
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid request body")
