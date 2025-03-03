from typing import Annotated
from fastapi import APIRouter, Depends, status

from docs.open_api_specs.routes.qr_code import (
    create_qr_code,
    get_qr_code_details,
    get_qr_code_list,
    update_qr_code,
    delete_qr_code,
)
from src.dependencies.auth.get_user import get_current_user
from src.dependencies.services.qr_code_service import get_qr_code_service
from src.dependencies.orchestration_services.qr_code_creation_orchestrator import get_qr_code_creation_orchestrator
from src.schemes.pagination import PaginationParams
from src.schemes.qr_code.request_bodies.update import UpdateQRCode, UpdateQRCodeCustomization
from src.schemes.qr_code.response_bodies.update import UpdateQRCodeResponseBody
from src.services.qr_code.abstract_qr_code_service import AbstractQRCodeService
from src.services.orchestration.qr_code.create_qr_code_abstract import AbstractQRCodeCreationOrchestrator
from src.models.user import User
from src.schemes.qr_code.request_bodies.create import CreateQRCodeRequestBody
from src.schemes.qr_code.response_bodies.create import CreateQRCodeResponse
from src.schemes.qr_code.base import BaseQRCodeSchema
from src.schemes.qr_code.response_bodies.details import QRCodeDetailsResponse
from src.schemes.qr_code.response_bodies.list import QRCodeListResponse

router = APIRouter(
    prefix='/qr-codes',
    tags=['qr-codes'],
)


@router.post('/', response_model=CreateQRCodeResponse, status_code=status.HTTP_201_CREATED, **create_qr_code.specs)
async def create_qr_code(
        create_qr_code_payload: CreateQRCodeRequestBody,
        user: Annotated[User, Depends(get_current_user)],
        qr_code_creation_orchestrator: Annotated[
            AbstractQRCodeCreationOrchestrator, Depends(get_qr_code_creation_orchestrator)
        ],
):
    created_qr_code = await qr_code_creation_orchestrator.create_qr_code(create_qr_code_payload, user)
    return CreateQRCodeResponse(created_item=BaseQRCodeSchema(**created_qr_code.model_dump()))


@router.get("/", response_model=QRCodeListResponse, **get_qr_code_list.specs)
async def get_qr_code_list(
        pagination_params: Annotated[PaginationParams, Depends(PaginationParams)],
        user: Annotated[User, Depends(get_current_user)],
        qr_code_service: Annotated[AbstractQRCodeService, Depends(get_qr_code_service)],
):
    items, pagination_response = await qr_code_service.get_qr_codes_with_links(user, pagination_params)
    return {
        "items": items,
        "pagination": pagination_response,
    }


@router.get('/{qr_code_id}', response_model=QRCodeDetailsResponse, **get_qr_code_details.specs)
async def get_qr_code_details(
        qr_code_id: int,
        user: Annotated[User, Depends(get_current_user)],
        qr_code_service: Annotated[AbstractQRCodeService, Depends(get_qr_code_service)],
):
    qr_code = await qr_code_service.get_qr_code_with_link(qr_code_id, user)
    return qr_code


@router.put('/{qr_code_id}', response_model=UpdateQRCodeResponseBody, **update_qr_code.specs)
async def update_qr_code(
        qr_code_id: int,
        data_to_update: UpdateQRCode | UpdateQRCodeCustomization,
        user: Annotated[User, Depends(get_current_user)],
        qr_code_service: Annotated[AbstractQRCodeService, Depends(get_qr_code_service)],
):
    updated_qr_code = await qr_code_service.update_qr_code(qr_code_id, user, data_to_update)
    return {"updated_item": updated_qr_code}


@router.delete('/{qr_code_id}', status_code=status.HTTP_204_NO_CONTENT, **delete_qr_code.specs)
async def delete_qr_code(
        qr_code_id: int,
        user: Annotated[User, Depends(get_current_user)],
        qr_code_service: Annotated[AbstractQRCodeService, Depends(get_qr_code_service)],
):
    await qr_code_service.delete_qr_code(qr_code_id, user)
