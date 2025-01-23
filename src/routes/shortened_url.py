from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from src.core.containers import Container
from src.dependencies.auth import get_current_user
from src.models.user import User
from src.schemes.shortened_url.response_bodies.retrieve import ShortenedUrlDetailsResponseSchema, \
    ShortenedUrlListResponseSchema
from src.schemes.shortened_url.response_bodies.update import UpdateShortenedUrlResponseSchema
from src.schemes.shortened_url.response_bodies.create import CreateShortenedUrlResponseSchema
from src.schemes.shortened_url.request_bodies.update import UpdateShortenedUrlSchema
from src.schemes.shortened_url.request_bodies.create import CreateShortenedUrlRequestBody
from src.schemes.pagination import PaginationParams
from src.services.shortened_url.abstract_url_service import AbstractURLService
from src.services.orchestration.shortened_url.url_update_abstract import AbstractUrlUpdateOrchestrator
from src.services.orchestration.shortened_url.url_delete_abstract import AbstractUrlDeleteOrchestrator

router = APIRouter(
    prefix='/urls',
    tags=['shortened-url'],
)


@router.post("/", response_model=CreateShortenedUrlResponseSchema, status_code=status.HTTP_201_CREATED)
@inject
async def create_shortened_url(url_data: CreateShortenedUrlRequestBody,
                               user: User = Depends(get_current_user),
                               url_service: AbstractURLService = Depends(Provide[Container.url_service])
                               ):
    created_url = await url_service.create_shortened_url(url_data, user)
    return CreateShortenedUrlResponseSchema(**created_url.model_dump())

@router.get("/", response_model=ShortenedUrlListResponseSchema)
@inject
async def get_all_shortened_urls(pagination_params: Annotated[PaginationParams, Depends(PaginationParams)],
                                 user: User = Depends(get_current_user),
                                 url_service: AbstractURLService = Depends(Provide[Container.url_service]),
                                 ):
    """
    Returns all user's shortened urls.
    """
    items, pagination_response = await url_service.get_shortened_url_list(user, pagination_params)
    return {
        "items": items,
        "pagination": pagination_response,
    }

@router.get('/{short_code}', response_model=ShortenedUrlDetailsResponseSchema)
@inject
async def get_shortened_url_details(short_code: str,
                                    user: User = Depends(get_current_user),
                                    url_service: AbstractURLService = Depends(Provide[Container.url_service])
                                    ):
    shortened_url = await url_service.get_shortened_url_details(short_code, user)
    return {
        "item": shortened_url,
    }


@router.put("/{short_code}",
            response_model=UpdateShortenedUrlResponseSchema, status_code=status.HTTP_200_OK)
@inject
async def update_shortened_url(short_code: str,
                               url_data: UpdateShortenedUrlSchema,
                               user: User = Depends(get_current_user),
                               url_update_orchestrator: AbstractUrlUpdateOrchestrator \
                                       = Depends(Provide[Container.url_update_orchestrator]),
                               ):
    updated_url = await url_update_orchestrator.update_url(short_code, url_data, user)
    return UpdateShortenedUrlResponseSchema(**updated_url.model_dump())


@router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_shortened_url(
        short_code: str,
        user: User = Depends(get_current_user),
        url_delete_orchestrator: AbstractUrlDeleteOrchestrator \
                = Depends(Provide[Container.url_delete_orchestrator]),
):
    await url_delete_orchestrator.delete_url(short_code, user)
