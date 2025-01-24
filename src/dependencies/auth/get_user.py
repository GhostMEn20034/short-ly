from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.dependencies.services.auth_service import get_auth_service
from src.models.user import User
from src.services.auth.abstract import AbstractAuthService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
    scheme_name="JWT"
)

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        auth_service: AbstractAuthService = Depends(get_auth_service)) -> User:
    return await auth_service.get_user_from_token(token)