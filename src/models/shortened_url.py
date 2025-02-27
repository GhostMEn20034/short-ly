from datetime import datetime, UTC
from sqlmodel import Field, Column, Integer, VARCHAR, Boolean, ForeignKey, Relationship, TIMESTAMP
from pydantic import HttpUrl

from .user import User
from .base import BaseModel


class ShortenedUrl(BaseModel, table=True):
    __tablename__ = 'shortened_url'

    id: int | None = Field(sa_column=Column("id", Integer, primary_key=True, autoincrement=True))
    friendly_name: str = Field(sa_column=Column("friendly_name", VARCHAR(40), nullable=False))
    is_short_code_custom: bool = Field(sa_column=Column("is_short_code_custom", Boolean, default=False))
    short_code: str = Field(sa_column=Column("short_code", VARCHAR(20), unique=True, nullable=False))
    long_url: HttpUrl = Field(sa_column=Column("long_url", VARCHAR(2083), nullable=False))

    # Relationship to the User model
    user_id: int = Field(
        sa_column=Column(
            "user_id",
            Integer,
            ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    user: User = Relationship(back_populates="shortened_urls")

    # Relationship to the QRCode model
    qr_code: "QRCode" = Relationship(back_populates="link", cascade_delete=True)

    created_at: datetime | None = Field(
        sa_column=Column(
            "created_at", TIMESTAMP(timezone=True),
            default=lambda: datetime.now(UTC),
            nullable=False,
            index=True,
        )
    )
