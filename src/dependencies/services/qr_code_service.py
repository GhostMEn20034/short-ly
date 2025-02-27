from typing import Annotated
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.database import get_session
from src.repositories.unit_of_work.implementation import UnitOfWork
from src.repositories.qr_code.qr_code_repository import QRCodeRepository
from src.services.qr_code.abstract_qr_code_service import AbstractQRCodeService
from src.services.qr_code.qr_code_service import QRCodeService


async def get_qr_code_service(db_session: Annotated[AsyncSession, Depends(get_session)],) -> AbstractQRCodeService:
    uow = UnitOfWork(db_session)
    qr_code_repository = QRCodeRepository(db_session)

    return QRCodeService(
        uow,
        qr_code_repository
    )
