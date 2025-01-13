from typing import Optional
from pydantic import constr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_CONNECTION_STRING: constr(strip_whitespace=True)
    JWT_SECRET_KEY: constr(strip_whitespace=True)
    REDIS_HOST: constr(strip_whitespace=True)
    REDIS_PASSWORD: Optional[constr(strip_whitespace=True)] = None
    REDIS_PORT: int = 6379


settings = Settings()
