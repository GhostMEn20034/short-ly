from datetime import datetime

from pydantic import BaseModel, constr, HttpUrl


class BaseShortenedUrlModel(BaseModel):
    id: int
    friendly_name: constr(max_length=40, strip_whitespace=True)
    is_short_code_custom: bool
    short_code: constr(max_length=20, strip_whitespace=True) = None
    long_url: HttpUrl
    created_at: datetime
