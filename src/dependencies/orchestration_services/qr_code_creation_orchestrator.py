from typing import Annotated
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.containers import Container
from src.core.database import get_session
# Repositories & Unit Of Work
from src.repositories.qr_code.qr_code_repository import QRCodeRepository
from src.repositories.unit_of_work.implementation import UnitOfWork
from src.repositories.shortened_url.url_repository import URLRepositorySQL
# Services
from src.services.short_code_generator.implementation import ShortCodeGenerator
from src.services.shortened_url.url_service import URLService
from src.services.qr_code.qr_code_service import QRCodeService
# Services-orchestrators
from src.services.orchestration.qr_code.create_qr_code_abstract import AbstractQRCodeCreationOrchestrator
from src.services.orchestration.qr_code.create_qr_code_implementation import QRCodeCreationOrchestrator


@inject
async def get_qr_code_creation_orchestrator(
        db_session: Annotated[AsyncSession, Depends(get_session)],
        short_code_generator: ShortCodeGenerator = Depends(Provide[Container.short_code_generator]),
) -> AbstractQRCodeCreationOrchestrator:
    uow = UnitOfWork(db_session)
    url_repository = URLRepositorySQL(db_session)
    qr_code_repository = QRCodeRepository(db_session)

    url_service = URLService(
        uow, url_repository,
        short_code_generator,
    )

    qr_code_service = QRCodeService(uow, qr_code_repository)

    qr_code_creation_orchestrator = QRCodeCreationOrchestrator(
        uow, url_service, qr_code_service
    )

    return qr_code_creation_orchestrator
