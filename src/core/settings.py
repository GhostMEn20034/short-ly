from pydantic import constr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_CONNECTION_STRING: constr(strip_whitespace=True)
    JWT_SECRET_KEY: constr(strip_whitespace=True)


settings = Settings()
