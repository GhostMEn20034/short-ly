from dependency_injector import providers, containers

# Pooled DB connections
from .database import get_session
from redis.asyncio import Redis
# Configs
from .settings import settings
from .configs.jwt_handler_config import JWTHandlerConfig
# Utils
from src.utils.auth.jwt_handler import JWTHandler
# Repositories & Unit Of work
from src.repositories.user.user_repository import UserRepositorySQL
from src.repositories.shortened_url.url_repository import URLRepositorySQL
from src.repositories.unit_of_work.implementation import UnitOfWork
# Services
from src.services.auth.auth_service import AuthService
from src.services.user.user_service import UserService
from src.services.short_code_generator.implementation import ShortCodeGenerator
from src.services.shortened_url.url_service import URLService
from src.services.cache.redis_cache import RedisCacheService
# Orchestration services
from src.services.orchestration.shortened_url.url_retrieval_implementation import UrlRetrievalOrchestrator
from src.services.orchestration.shortened_url.url_update_implementation import UrlUpdateOrchestrator
from src.services.orchestration.shortened_url.url_delete_implementation import UrlDeleteOrchestrator


class Container(containers.DeclarativeContainer):
    # Pooled DB connections
    db_session = providers.Resource(get_session)
    redis_pool = providers.Singleton(
        Redis,
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        decode_responses=True,
    )
    # Configs
    jwt_config = providers.Singleton(JWTHandlerConfig, secret_key=settings.JWT_SECRET_KEY)
    # Utils
    jwt_handler = providers.Singleton(JWTHandler, config=jwt_config)

    # Repositories
    user_repository = providers.Factory(UserRepositorySQL, session=db_session)
    url_repository = providers.Factory(URLRepositorySQL, session=db_session)

    unit_of_work = providers.Factory(
        UnitOfWork,
        session=db_session,
        user_repository=user_repository,
        url_repository=url_repository,
    )

    # Services
    short_code_generator = providers.Singleton(ShortCodeGenerator)

    auth_service = providers.Factory(
        AuthService,
        jwt_handler=jwt_handler, uow=unit_of_work
    )
    user_service = providers.Factory(
        UserService,
        uow=unit_of_work
    )
    url_service = providers.Factory(
        URLService,
        uow=unit_of_work,
        short_code_generator=short_code_generator,
    )
    redis_cache_service = providers.Factory(
        RedisCacheService,
        redis=redis_pool,
    )

    # Orchestration services
    url_retrieval_orchestrator = providers.Factory(
        UrlRetrievalOrchestrator,
        url_service=url_service,
        cache_service=redis_cache_service,
    )

    url_update_orchestrator = providers.Factory(
        UrlUpdateOrchestrator,
        url_service=url_service,
        cache_service=redis_cache_service,
    )

    url_delete_orchestrator = providers.Factory(
        UrlDeleteOrchestrator,
        url_service=url_service,
        cache_service=redis_cache_service,
    )
