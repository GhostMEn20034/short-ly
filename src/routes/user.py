from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.dependencies.services.user_service import get_user_service
from src.models.user import User
from src.schemes.user import UserCreate, UserReadSchema, UserUpdateSchema, ChangePasswordSchema, ChangeEmailSchema
from src.services.user.abstract import AbstractUserService
from src.dependencies.auth.get_user import get_current_user


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserReadSchema)
async def signup(user_data: UserCreate,
                 user_service: Annotated[AbstractUserService, Depends(get_user_service)],
                 ):
    return await user_service.user_signup(user_data)


@router.get('/details', response_model=UserReadSchema)
async def get_user_details(user: Annotated[User, Depends(get_current_user)],):
    return UserReadSchema(**user.model_dump())


@router.put('/update', response_model=UserReadSchema)
async def update_user(
        user_update_data: UserUpdateSchema,
        user: Annotated[User, Depends(get_current_user)],
        user_service: Annotated[AbstractUserService, Depends(get_user_service)],
):
    return await user_service.update_user(user, user_update_data)


@router.put('/change-email', response_model=UserReadSchema)
async def change_email(
        data_to_update: ChangeEmailSchema,
        user: Annotated[User, Depends(get_current_user)],
        user_service: Annotated[AbstractUserService, Depends(get_user_service)],
):
    return await user_service.change_email(user, data_to_update.email)


@router.put('/change-password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
        change_password_data: ChangePasswordSchema,
        user: Annotated[User, Depends(get_current_user)],
        user_service: Annotated[AbstractUserService, Depends(get_user_service)],
):
    await user_service.change_password(user, change_password_data)
