from datetime import datetime, date, UTC
from typing import List
from pydantic import EmailStr
from sqlmodel import Field, Column, String, Date, TIMESTAMP, Integer, Relationship

from .base import BaseModel


class User(BaseModel, table=True):
    __tablename__ = 'user'

    id: int | None = Field(sa_column=Column("id", Integer, primary_key=True, autoincrement=True))
    email: EmailStr = Field(sa_column=Column("email", String(256), unique=True, index=True))
    first_name: str = Field(sa_column=Column("first_name", String(128)))
    last_name: str = Field(sa_column=Column("last_name", String(128), nullable=True))
    password: str = Field(sa_column=Column("password", String(256)))

    date_of_birth: date | None = Field(sa_column=Column("date_of_birth", Date, nullable=True))

    created_at: datetime | None = Field(
        sa_column=Column(
            "created_at", TIMESTAMP(timezone=True),
            default=lambda: datetime.now(UTC),
            nullable=False
        )
    )
    updated_at: datetime | None = Field(
        sa_column=Column(
            "updated_at", TIMESTAMP(timezone=True),
            default=lambda: datetime.now(UTC),
            onupdate=lambda: datetime.now(UTC),
            nullable=False
        )
    )

    shortened_urls: List["ShortenedUrl"] = Relationship(back_populates="user", cascade_delete=True)