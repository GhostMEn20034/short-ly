from dependency_injector import providers, containers

# Pooled DB connections
from redis.asyncio import Redis
# Configs
from .settings import settings
from .configs.jwt_handler_config import JWTHandlerConfig
# Utils
from src.utils.auth.jwt_handler import JWTHandler
# Services
from src.services.short_code_generator.implementation import ShortCodeGenerator
from src.services.cache.redis_cache import RedisCacheService


class Container(containers.DeclarativeContainer):
    # Pooled DB connections
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

    # Services
    short_code_generator = providers.Singleton(ShortCodeGenerator)

    redis_cache_service = providers.Factory(
        RedisCacheService,
        redis=redis_pool,
    )