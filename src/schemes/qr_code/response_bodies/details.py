from datetime import datetime, UTC
from pydantic import constr, HttpUrl

from pydantic import BaseModel
from src.schemes.qr_code.base import BaseQRCodeSchema


class JoinedShortenedUrl(BaseModel):
    friendly_name: str
    short_code: constr(max_length=20, strip_whitespace=True) = None
    long_url: HttpUrl
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "friendly_name": "My link to Twitch",
                "short_code": "twitch-tv",
                "long_url": "https://twitch.tv",
                "created_at": datetime.now(tz=UTC),
            }
        }

class QRCodeDetailsResponse(BaseQRCodeSchema):
    link: JoinedShortenedUrl
