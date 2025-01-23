from typing import Optional, List
from pydantic import constr, field_validator, model_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_CONNECTION_STRING: constr(strip_whitespace=True)
    JWT_SECRET_KEY: constr(strip_whitespace=True)
    REDIS_HOST: constr(strip_whitespace=True)
    REDIS_PASSWORD: Optional[constr(strip_whitespace=True)] = None
    REDIS_PORT: int = 6379
    CORS_ALLOWED_ORIGINS: List[constr(strip_whitespace=True)] = ["http://localhost:5173"]


settings = Settings()
