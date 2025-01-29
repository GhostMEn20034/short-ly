from pydantic import BaseModel, constr, HttpUrl


class UpdateShortenedUrlSchema(BaseModel):
    friendly_name: constr(max_length=40, strip_whitespace=True)
    long_url: HttpUrl

    class Config:
        json_schema_extra = {
            "example": {
                "friendly_name": "My link to Twitch",
                "long_url": "https://twitch.tv"
            }
        }
