from typing import Annotated
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.database import get_session
from src.repositories.unit_of_work.implementation import UnitOfWork
from src.repositories.user.user_repository import UserRepositorySQL
from src.services.user.abstract import AbstractUserService
from src.services.user.user_service import UserService


async def get_user_service(db_session: Annotated[AsyncSession, Depends(get_session)],) -> AbstractUserService:
    uow = UnitOfWork(db_session)
    user_repository = UserRepositorySQL(db_session)

    return UserService(
        uow,
        user_repository
    )
