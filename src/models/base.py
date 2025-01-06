from sqlmodel import SQLModel

from src.utils.str_utils import to_camel_case


class BaseModel(SQLModel):
    """
    Base SQL model class.
    """

    class Config:
        alias_generator = to_camel_case
        populate_by_name = True
        arbitrary_types_allowed = True