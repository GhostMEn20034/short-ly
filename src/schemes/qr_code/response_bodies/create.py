from pydantic import BaseModel, Field

from ..base import BaseQRCodeSchema

class CreateQRCodeResponse(BaseModel):
    created_item: BaseQRCodeSchema = Field(..., alias="createdItem")

    class Config:
        populate_by_name = True

