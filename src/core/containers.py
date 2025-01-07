from dependency_injector import providers, containers

from .database import get_session
from .settings import settings
from .configs.jwt_handler_config import JWTHandlerConfig
from src.utils.auth.jwt_handler import JWTHandler
# Repositories & Unit Of work
from src.repositories.user.user_repository_sql import UserRepositorySQL
from src.repositories.unit_of_work.implementation import UnitOfWork
# Services
from src.services.auth.auth_service import AuthService
from src.services.user.user_service import UserService


class Container(containers.DeclarativeContainer):
    db_session = providers.Resource(get_session)

    jwt_config = providers.Singleton(JWTHandlerConfig, secret_key=settings.JWT_SECRET_KEY)
    jwt_handler = providers.Singleton(JWTHandler, config=jwt_config)

    user_repository = providers.Factory(UserRepositorySQL, session=db_session)

    unit_of_work = providers.Factory(
        UnitOfWork,
        session=db_session,
        user_repository=user_repository,
    )

    auth_service = providers.Factory(
        AuthService,
        jwt_handler=jwt_handler, uow=unit_of_work
    )
    user_service = providers.Factory(
        UserService,
        uow=unit_of_work
    )
