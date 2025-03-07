from fastapi import HTTPException, status

from src.models.user import User
from src.models.shortened_url import ShortenedUrl
from src.models.qr_code import QRCode
from src.repositories.unit_of_work.abstract import AbstractUnitOfWork
from src.schemes.qr_code.request_bodies.create import CreateQRCodeRequestBody
from src.utils.error_utils import generate_error_response
from .create_qr_code_abstract import AbstractQRCodeCreationOrchestrator
from src.services.shortened_url.abstract_url_service import AbstractURLService
from src.services.qr_code.abstract_qr_code_service import AbstractQRCodeService


class QRCodeCreationOrchestrator(AbstractQRCodeCreationOrchestrator):
    def __init__(self,
                 uow: AbstractUnitOfWork,
                 url_service: AbstractURLService,
                 qr_code_service: AbstractQRCodeService,
                 ):
        self._uow = uow
        self._url_service = url_service
        self._qr_code_service = qr_code_service

    async def create_qr_code(self, create_qr_code_payload: CreateQRCodeRequestBody, creator: User) -> QRCode:
        async with self._uow:
            self._uow.prevent_commit()

            shortened_url = await self._get_or_create_shortened_url(create_qr_code_payload, creator)
            created_qr_code = await self._qr_code_service.create_qr_code(
                create_qr_code_payload.qr_code, shortened_url, creator.id,
            )

            self._uow.allow_commit()
            await self._uow.commit()

            return created_qr_code

    async def _get_or_create_shortened_url(
            self, create_qr_code_payload: CreateQRCodeRequestBody, creator: User) -> ShortenedUrl:
        shortened_url: ShortenedUrl
        if create_qr_code_payload.link_short_code is not None:
            shortened_url, qr_code = await self._url_service.get_shortened_url_details(
                create_qr_code_payload.link_short_code, creator
            )

            if qr_code is not None:
                error_details = generate_error_response(
                    location=["body", "linkShortCode"],
                    message="Unable to create a QR Code for the link",
                    reason="There's a qr code for this link already",
                    input_value=create_qr_code_payload.link_short_code,
                    error_type="domain_error"
                )

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=[error_details, ],
                )
        else:
            shortened_url = await self._url_service.create_shortened_url(create_qr_code_payload.link_to_create, creator)

        return shortened_url
