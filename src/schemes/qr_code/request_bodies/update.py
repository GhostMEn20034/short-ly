from pydantic import BaseModel, HttpUrl, constr


class UpdateQRCode(BaseModel):
    title: constr(min_length=1, max_length=40)


class UpdateQRCodeCustomization(BaseModel):
    image: HttpUrl | None = None
    customization: dict
