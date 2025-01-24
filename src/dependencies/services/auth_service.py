from typing import Annotated
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.containers import Container
from src.core.database import get_session
from src.repositories.unit_of_work.implementation import UnitOfWork
from src.repositories.user.user_repository import UserRepositorySQL
from src.services.auth.abstract import AbstractAuthService
from src.services.auth.auth_service import AuthService
from src.utils.auth.jwt_handler import JWTHandler


@inject
async def get_auth_service(
        db_session: Annotated[AsyncSession, Depends(get_session)],
        jwt_handler: JWTHandler = Depends(Provide[Container.jwt_handler]),
) -> AbstractAuthService:
    uow = UnitOfWork(db_session)
    user_repository = UserRepositorySQL(db_session)


    auth_service = AuthService(
        jwt_handler=jwt_handler, uow=uow,
        user_repository=user_repository,
    )
    return auth_service