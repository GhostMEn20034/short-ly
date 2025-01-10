from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, HTTPException

from src.core.containers import Container
from src.dependencies.auth import get_current_user
from src.models.user import User
from src.schemes.shortened_url import (
    CreateShortenedUrlResponseSchema, CreateShortenedUrlSchema,
    UpdateShortenedUrlResponseSchema, UpdateShortenedUrlSchema,
    ShortenedUrlDetailsResponseSchema,
)
from src.services.shortened_url.abstract_url_service import AbstractURLService

router = APIRouter(
    prefix='/urls',
    tags=['shorted-url'],
)


@router.post("/", response_model=CreateShortenedUrlResponseSchema, status_code=status.HTTP_201_CREATED)
@inject
async def create_shortened_url(url_data: CreateShortenedUrlSchema,
                               user: User = Depends(get_current_user),
                               url_service: AbstractURLService = Depends(Provide[Container.url_service])
                               ):
    created_url = await url_service.create_shortened_url(url_data, user)
    return CreateShortenedUrlResponseSchema(**created_url.model_dump())


@router.get('/{short_code}', response_model=ShortenedUrlDetailsResponseSchema)
@inject
async def get_shortened_url_details(short_code: str,
                                    user: User = Depends(get_current_user),
                                    url_service: AbstractURLService = Depends(Provide[Container.url_service])
                                    ):
    return await url_service.get_shortened_url_details(short_code, user)


@router.put("/{short_code}",
            response_model=UpdateShortenedUrlResponseSchema, status_code=status.HTTP_200_OK)
@inject
async def update_shortened_url(short_code: str,
                               url_data: UpdateShortenedUrlSchema,
                               user: User = Depends(get_current_user),
                               url_service: AbstractURLService = Depends(Provide[Container.url_service]),
                               ):
    updated_url = await url_service.update_shortened_url(short_code, url_data, user)
    return UpdateShortenedUrlResponseSchema(**updated_url.model_dump())


@router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_shortened_url(
        short_code: str,
        user: User = Depends(get_current_user),
        url_service: AbstractURLService = Depends(Provide[Container.url_service]),
):
    deleted = await url_service.delete_shortened_url(short_code, user)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
