from pydantic import BaseModel, constr


class UpdateShortenedUrlSchema(BaseModel):
    friendly_name: constr(max_length=40, strip_whitespace=True)
