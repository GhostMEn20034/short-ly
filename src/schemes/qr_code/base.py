from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class BaseQRCodeSchema(BaseModel):
    id: int | None = Field(None, alias='id')
    title: str = Field(..., alias='title')
    image: HttpUrl | None = Field(None, alias="image")
    customization: dict = Field(..., alias="customization")
    user_id: int = Field(..., alias='userId')
    link_id: int = Field(..., alias='linkId')
    created_at: datetime | None = Field(..., alias='createdAt')
    updated_at: datetime | None = Field(..., alias='updatedAt')

    class Config:
        populate_by_name = True