from datetime import datetime, UTC
from pydantic import HttpUrl
from sqlmodel import Field, Column, Integer, VARCHAR, ForeignKey, Relationship, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSON

from .user import User
from .shortened_url import ShortenedUrl
from .base import BaseModel


class QRCode(BaseModel, table=True):
    __tablename__ = 'qr_code'
    id: int | None = Field(sa_column=Column("id", Integer, primary_key=True, autoincrement=True))
    title: str = Field(sa_column=Column("title", VARCHAR(40), nullable=False))
    image: HttpUrl | None = Field(sa_column=Column("image", VARCHAR(2083), nullable=True))
    customization: dict = Field(sa_column=Column("customization", JSON, nullable=False))

    # Relationship to the User model
    user_id: int = Field(
        sa_column=Column(
            "user_id", Integer,
            ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False
        ),
    )
    user: User = Relationship(back_populates="qr_codes",
                              sa_relationship_kwargs={"lazy": "selectin"})

    # Relationship to the ShortenedUrl model
    link_id: int = Field(
        sa_column=Column(
            "link_id", Integer,
            ForeignKey("shortened_url.id", ondelete="CASCADE"),
            unique=True,
            nullable=False,
        ),
    )
    link: ShortenedUrl = Relationship(back_populates="qr_code",
                                      sa_relationship_kwargs={"lazy": "selectin"})

    # Timestamps
    created_at: datetime | None = Field(
        sa_column=Column(
            "created_at", TIMESTAMP(timezone=True),
            default=lambda: datetime.now(UTC),
            nullable=False,
            index=True,
        ),
    )
    updated_at: datetime | None = Field(
        sa_column=Column(
            "updated_at", TIMESTAMP(timezone=True),
            default=lambda: datetime.now(UTC),
            onupdate=lambda: datetime.now(UTC),
            nullable=False,
            index=True,
        ),
    )
