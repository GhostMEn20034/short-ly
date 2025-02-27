from typing import Any
from pydantic import BaseModel, constr, HttpUrl, Field, model_validator

from src.schemes.shortened_url.request_bodies.create import CreateShortenedUrlRequestBody


class CreateQRCodeSchema(BaseModel):
    image: HttpUrl | None = None
    customization: dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "image": "https://i.imgur.com/CF422bf.jpeg",
                "customization": {
                    "width": 300,
                    "height": 300,
                }
            }
        }

class CreateQRCodeRequestBody(BaseModel):
    link_to_create: CreateShortenedUrlRequestBody | None = Field(None, alias='linkToCreate')
    link_short_code: constr(min_length=1, strip_whitespace=True) | None = Field(None, alias='linkShortCode')
    qr_code: CreateQRCodeSchema = Field(..., alias='qrCode')

    @model_validator(mode='after')
    def validate_link_data_presence(self):
        """
        If the client does not provide link short code, link_to_create object must be provided
        """
        if self.link_short_code is None and self.link_to_create is None:
            raise ValueError("Either link's short code or data to create a new link must be provided")

        return self

    class Config:
        populate_by_name = True
