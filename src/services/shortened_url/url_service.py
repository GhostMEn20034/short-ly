import math
from typing import Optional, Sequence, Tuple

from fastapi import HTTPException, status
from pydantic import HttpUrl

from .abstract_url_service import AbstractURLService
from src.schemes.shortened_url.request_bodies.update import UpdateShortenedUrlSchema
from src.schemes.shortened_url.request_bodies.create import CreateShortenedUrlRequestBody
from src.repositories.unit_of_work.abstract import AbstractUnitOfWork
from src.services.short_code_generator.abstract import AbstractShortCodeGenerator
from src.core.exceptions.shortened_url import MaxRetriesExceeded
from src.models.shortened_url import ShortenedUrl
from src.models.user import User
from src.schemes.pagination import PaginationParams, PaginationResponse
from src.repositories.shortened_url.abstract import AbstractURLRepositorySQL
from src.utils.error_utils import generate_error_response


class URLService(AbstractURLService):
    def __init__(self,
                 uow: AbstractUnitOfWork,
                 url_repository: AbstractURLRepositorySQL,
                 short_code_generator: AbstractShortCodeGenerator,
                 ):
        self._uow = uow
        self._url_repository = url_repository
        self._short_code_generator = short_code_generator

    async def _get_unique_short_code(self) -> str:
        """
        Generates and returns a unique short code.

        This method iterates through a series of generated short codes,
        checking each one for existence in the database.
        Returns the first unique short code found, or raises MaxRetriesExceeded exception
        if no unique code is found within the allowed number of retries.
        """
        for generated_short_code in self._short_code_generator.generate_short_code(code_length=8, max_retries=5):
            exists = await self._url_repository.is_shortened_url_exist(generated_short_code)
            if not exists:
                return generated_short_code

    async def create_shortened_url(self, data: CreateShortenedUrlRequestBody, owner: User) -> ShortenedUrl:
        """
        Creates shortened url using given data
        returns created shortened url if everything is fine.
        If shortened url is not created returns None
        """
        is_short_code_custom = data.is_short_code_custom
        short_code = data.short_code

        # If the user doesn't want to use custom short code,
        # then generate random one
        if not is_short_code_custom:
            # Program has 5 attempts to create unique short code.
            # If all 5 codes are not unique, then return None, which indicates that shorted url is not created.
            try:
                short_code = await self._get_unique_short_code()
            except MaxRetriesExceeded:
                error_details = generate_error_response(
                    location=["body", "short_code"],
                    message="Unable to generate short code",
                    reason="Currently, server cannot generate short code",
                    input_value="",
                    error_type="internal_error"
                )

                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=[error_details, ],
                )
        else:
            exists = await self._url_repository.is_shortened_url_exist(short_code)
            if exists:
                error_details = generate_error_response(
                    location=["body", "short_code"],
                    message="Unable to create a shortened url",
                    reason="Entered short code already exists",
                    input_value=short_code,
                    error_type="domain_error"
                )

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=[error_details, ],
                )


        shortened_url = ShortenedUrl(
            friendly_name=data.friendly_name,
            is_short_code_custom=is_short_code_custom,
            short_code=short_code,
            long_url=str(data.long_url),
            user_id=owner.id,
        )

        created_shortened_url = await self._url_repository.add(shortened_url)
        await self._uow.commit()

        return created_shortened_url

    async def get_shortened_url_list(self, user: User, pagination_params: PaginationParams) \
                                                                   -> Tuple[Sequence[ShortenedUrl], PaginationResponse]:

        items, total_count = await self._url_repository.get_paginated_url_list(user.id, pagination_params)
        total_pages = math.ceil(total_count / pagination_params.page_size)

        # By default, pagination should always result
        # in at least one "page" (even if it's empty), so this block of code ensures that total_pages is at least 1.
        if total_pages < 1:
            total_pages = 1

        pagination_response = PaginationResponse(
            current_page=pagination_params.page,
            page_size=pagination_params.page_size,
            total_pages=total_pages,
            total_items=total_count,
        )

        return items, pagination_response

    async def get_shortened_url_details(self, short_code: str, owner: User) -> Optional[ShortenedUrl]:
        shortened_url = await self._url_repository.get_by_short_code(short_code)
        if not shortened_url:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if owner.id != shortened_url.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not the owner of this shortened url"
            )

        return shortened_url

    async def get_long_url(self, short_code: str) -> HttpUrl:
        shortened_url = await self._url_repository.get_by_short_code(short_code)
        if not shortened_url:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail={"short_code": f"Url with short code {short_code} doesn't exist"})

        return shortened_url.long_url

    async def update_shortened_url(self, short_code: str, data: UpdateShortenedUrlSchema, owner: User) -> ShortenedUrl:
        shortened_url = await self._url_repository.get_by_short_code(short_code)
        if not shortened_url:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if owner.id != shortened_url.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not the owner of this shortened url"
            )

        # update shortened url's friendly name
        shortened_url.friendly_name = data.friendly_name
        shortened_url.long_url = str(data.long_url)
        updated_shortened_url = await self._url_repository.update(shortened_url)
        await self._uow.commit()

        return updated_shortened_url

    async def delete_shortened_url(self, short_code: str, owner: User) -> bool:
        shortened_url = await self._url_repository.get_by_short_code(short_code)
        if not shortened_url:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if owner.id != shortened_url.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not the owner of this shortened url"
            )

        await self._url_repository.delete(shortened_url)
        await self._uow.commit()

        return True
