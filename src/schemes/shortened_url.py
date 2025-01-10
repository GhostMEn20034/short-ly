from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr, HttpUrl, field_validator
from pydantic_core.core_schema import ValidationInfo

from .consts import reserved_words


class CreateShortenedUrlSchema(BaseModel): # Request Body
    friendly_name: constr(max_length=40, strip_whitespace=True)
    is_short_code_custom: bool
    short_code: constr(min_length=8, max_length=20, strip_whitespace=True) = None
    long_url: HttpUrl

    @field_validator('short_code')
    def short_code_is_valid(cls, value, info: ValidationInfo):
        """Ensure that shortcode is valid if the user specified that the short code is custom"""
        is_short_code_custom = info.data["is_short_code_custom"]

        if is_short_code_custom:
            cls._validate_short_code_presence(value)
            cls._validate_short_code_reserved(value)

        return value

    @classmethod
    def _validate_short_code_presence(cls, value: Optional[str]):
        if value is None:
            raise ValueError("Enter a short code")

    @classmethod
    def _validate_short_code_reserved(cls, value: str):
        if value.lower() in reserved_words:
            raise ValueError(
                f"The short code '{value}' is reserved and cannot be used. Please choose a different short code.")


class UpdateShortenedUrlSchema(BaseModel): # Request Body
    friendly_name: constr(max_length=40, strip_whitespace=True)


class CreateShortenedUrlResponseSchema(BaseModel):
    id: int
    friendly_name: constr(max_length=40, strip_whitespace=True)
    is_short_code_custom: bool
    short_code: constr(max_length=20, strip_whitespace=True) = None
    long_url: HttpUrl
    created_at: datetime


class UpdateShortenedUrlResponseSchema(CreateShortenedUrlResponseSchema):
    pass

class ShortenedUrlDetailsResponseSchema(CreateShortenedUrlResponseSchema):
    pass
