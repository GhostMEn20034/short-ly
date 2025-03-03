from pydantic import BaseModel, Field

from src.schemes.qr_code.base import BaseQRCodeSchema


class UpdateQRCodeResponseBody(BaseModel):
    updated_item: BaseQRCodeSchema = Field(..., alias="updatedItem")

    class Config:
        populate_by_name = True
