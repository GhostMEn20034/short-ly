from typing import Annotated
from fastapi import APIRouter, Depends, status, Query

# Open API Specs
from docs.open_api_specs.routes.shortened_url import (
    create_url,
    update_url,
    delete_url,
    get_url_details,
    get_all_urls,
)
# Dependency Functions
from src.dependencies.auth.get_user import get_current_user
from src.dependencies.services.url_service import get_url_service
from src.dependencies.orchestration_services.url_update_orchestrator import get_url_update_orchestrator
from src.dependencies.orchestration_services.url_delete_orchestrator import get_url_delete_orchestrator
# Models
from src.models.user import User
# Schemes
from src.schemes.shortened_url.response_bodies.retrieve import ShortenedUrlDetailsResponseSchema, \
    ShortenedUrlListResponseSchema
from src.schemes.shortened_url.response_bodies.update import UpdateShortenedUrlResponseSchema
from src.schemes.shortened_url.response_bodies.create import CreateShortenedUrlResponseSchema
from src.schemes.shortened_url.request_bodies.update import UpdateShortenedUrlSchema
from src.schemes.shortened_url.request_bodies.create import CreateShortenedUrlRequestBody
from src.schemes.pagination import PaginationParams
from src.schemes.common import DatetimeRange
# Services
from src.services.shortened_url.abstract_url_service import AbstractURLService
from src.services.orchestration.shortened_url.url_update_abstract import AbstractUrlUpdateOrchestrator
from src.services.orchestration.shortened_url.url_delete_abstract import AbstractUrlDeleteOrchestrator


router = APIRouter(
    prefix='/urls',
    tags=['shortened-url'],
)


@router.post(
    "/",
    response_model=CreateShortenedUrlResponseSchema,
    status_code=status.HTTP_201_CREATED,
    **create_url.specs,
)
async def create_shortened_url(url_data: CreateShortenedUrlRequestBody,
                               user: Annotated[User, Depends(get_current_user)],
                               url_service: Annotated[AbstractURLService, Depends(get_url_service)],
                               ):
    created_url = await url_service.create_shortened_url(url_data, user)
    return CreateShortenedUrlResponseSchema(**created_url.model_dump())


@router.get(
    "/",
    response_model=ShortenedUrlListResponseSchema,
    **get_all_urls.specs,
)
async def get_all_shortened_urls(pagination_params: Annotated[PaginationParams, Depends(PaginationParams)],
                                 datetime_range_params: Annotated[DatetimeRange, Query()],
                                 user: Annotated[User, Depends(get_current_user)],
                                 url_service: Annotated[AbstractURLService, Depends(get_url_service)],
                                 ):
    """
    Returns all user's shortened urls.
    """
    items, pagination_response = await url_service.get_shortened_url_list(
        user, datetime_range_params, pagination_params
    )
    return {
        "items": items,
        "pagination": pagination_response,
    }


@router.get(
    '/{short_code}',
    response_model=ShortenedUrlDetailsResponseSchema,
    **get_url_details.specs,
)
async def get_shortened_url_details(short_code: str,
                                    user: Annotated[User, Depends(get_current_user)],
                                    url_service: Annotated[AbstractURLService, Depends(get_url_service)],
                                    ):
    shortened_url = await url_service.get_shortened_url_details(short_code, user)
    return {
        "item": shortened_url,
    }


@router.put(
    "/{short_code}",
    response_model=UpdateShortenedUrlResponseSchema,
    status_code=status.HTTP_200_OK,
    **update_url.specs,
)
async def update_shortened_url(short_code: str,
                               url_data: UpdateShortenedUrlSchema,
                               user: Annotated[User, Depends(get_current_user)],
                               url_update_orchestrator: Annotated[
                                   AbstractUrlUpdateOrchestrator, Depends(get_url_update_orchestrator)
                               ],
                               ):
    updated_url = await url_update_orchestrator.update_url(short_code, url_data, user)
    return UpdateShortenedUrlResponseSchema(**updated_url.model_dump())


@router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT, **delete_url.specs)
async def delete_shortened_url(
        short_code: str,
        user: Annotated[User, Depends(get_current_user)],
        url_delete_orchestrator: Annotated[
            AbstractUrlDeleteOrchestrator, Depends(get_url_delete_orchestrator)
        ],
):
    await url_delete_orchestrator.delete_url(short_code, user)
