from datetime import datetime, UTC

from pydantic import BaseModel, constr, HttpUrl


class BaseShortenedUrlModel(BaseModel):
    id: int
    friendly_name: constr(max_length=40, strip_whitespace=True)
    is_short_code_custom: bool
    short_code: constr(max_length=20, strip_whitespace=True) = None
    long_url: HttpUrl
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "friendly_name": "My link to Twitch",
                "is_short_code_custom": True,
                "short_code": "twitch-tv",
                "long_url": "https://twitch.tv",
                "created_at": datetime.now(tz=UTC),
            }
        }
