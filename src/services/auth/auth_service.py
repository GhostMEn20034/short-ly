import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .abstract import AbstractAuthService
from src.core.exceptions.tokens import InvalidTokenType
from src.repositories.unit_of_work.abstract import AbstractUnitOfWork
from src.utils.auth.jwt_handler import JWTHandler
from src.utils.password_utils import verify_password
from src.utils.error_utils import generate_error_response
from src.schemes.auth.token_data import AuthTokens, TokenPayload
from src.models.user import User
from src.repositories.user.abstract import AbstractUserRepository


class AuthService(AbstractAuthService):
    def __init__(self, jwt_handler: JWTHandler, uow: AbstractUnitOfWork, user_repository: AbstractUserRepository):
        self._jwt_handler = jwt_handler
        self._uow = uow
        self._user_repository = user_repository

    async def provide_tokens(self, form_data: OAuth2PasswordRequestForm) -> AuthTokens:
            user = await self._user_repository.get_by_email(form_data.username)

            if user is None:
                error_details = generate_error_response(
                    location=["body", "email"],
                    message="Incorrect email or password",
                    reason="Incorrect email or password",
                    input_value=form_data.username,
                    error_type="domain_error"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=[error_details, ],
                )

            hashed_password = user.password

            if not verify_password(form_data.password, hashed_password):
                error_details = generate_error_response(
                    location=["body", "password"],
                    message="Incorrect email or password",
                    reason="Incorrect email or password",
                    input_value=form_data.password,
                    error_type="domain_error"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=[error_details, ],
                )

            token_payload = {
                "id": user.id,
            }

            access_token = self._jwt_handler.create_access_token(token_payload.copy())
            refresh_token = self._jwt_handler.create_refresh_token(token_payload.copy())

            return AuthTokens(
                access_token=access_token,
                refresh_token=refresh_token
            )

    def _decode_token(self, token: str, token_type: str) -> TokenPayload:
        """
        Decodes a JWT token
        :param token: your token.
        :param token_type: token type ("access" or "refresh").
        :return: Decoded token's payload
        """
        try:

            if token_type == 'access':
                payload = self._jwt_handler.decode_access_token(token)
            else:
                payload = self._jwt_handler.decode_refresh_token(token)

        except (jwt.PyJWTError, InvalidTokenType):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenPayload(**payload)

    async def get_user_from_token(self, token: str) -> User:
        token_data = self._decode_token(token, token_type='access')

        user = await self._user_repository.get_by_id(token_data.id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )
        return user


    async def refresh_access_token(self, refresh_token: str) -> str:
        token_data = self._decode_token(refresh_token, token_type='refresh')

        user = await self._user_repository.get_by_id(token_data.id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )

        payload = {"id": user.id}

        return self._jwt_handler.create_access_token(payload)

    async def refresh_both_tokens(self, refresh_token: str) -> AuthTokens:
        token_data = self._decode_token(refresh_token, token_type='refresh')

        user = await self._user_repository.get_by_id(token_data.id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )

        payload = {"id": user.id}
        access_token = self._jwt_handler.create_access_token(payload.copy())
        refresh_token = self._jwt_handler.create_refresh_token(payload.copy())

        return AuthTokens(
            access_token=access_token,
            refresh_token=refresh_token,
        )