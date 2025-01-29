from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from docs.open_api_specs.routes.auth import login, refresh_tokens

from src.schemes.auth.token_data import RefreshTokensRequest, AuthTokens
from src.services.auth.abstract import AbstractAuthService
from src.dependencies.services.auth_service import get_auth_service

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post(
    '/token',
    response_model=AuthTokens,
    **login.specs,
)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service: AbstractAuthService = Depends(get_auth_service)
):
    return await auth_service.provide_tokens(form_data)

@router.post(
    '/token/refresh',
    response_model=AuthTokens,
    **refresh_tokens.specs,
)
async def refresh_tokens(
        refresh_tokens_req: RefreshTokensRequest,
        auth_service: AbstractAuthService = Depends(get_auth_service)
):

    return await auth_service.refresh_both_tokens(refresh_tokens_req.refresh_token)