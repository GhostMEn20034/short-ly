from typing import Annotated
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.containers import Container
from src.core.database import get_session
from src.repositories.unit_of_work.implementation import UnitOfWork
from src.repositories.shortened_url.url_repository import URLRepositorySQL
from src.services.short_code_generator.implementation import ShortCodeGenerator
from src.services.shortened_url.abstract_url_service import AbstractURLService
from src.services.shortened_url.url_service import URLService


@inject
async def get_url_service(
        db_session: Annotated[AsyncSession, Depends(get_session)],
        short_code_generator: ShortCodeGenerator = Depends(Provide[Container.short_code_generator]),
) -> AbstractURLService:
    uow = UnitOfWork(db_session)
    url_repository = URLRepositorySQL(db_session)

    url_service = URLService(
        uow, url_repository,
        short_code_generator,
    )

    return url_service
