from datetime import date, datetime, UTC
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, ValidationInfo


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    password1: str
    password2: str

    @field_validator('password1', 'password2')
    def password_length(cls, value: str):
        """Ensure password is at least 8 characters long."""
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return value

    @field_validator('password2')
    def passwords_match(cls, value, info: ValidationInfo):
        """Ensure both passwords match."""
        password1 = info.data.get("password1")  # Use the new approach to get value
        if password1 is None or value != password1:
            raise ValueError('Passwords do not match')
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "email": "your@email.com",
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": datetime.now(UTC),
                "password1": "your-pwd",
                "password2": "your-pwd"
            }
        }

class UserUpdateSchema(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": datetime.now(UTC),
            }
        }

class UserReadSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "email": "your@email.com",
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": datetime.now(UTC),
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC)
            }
        }

class ChangeEmailSchema(BaseModel):
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "email": "your@email.com",
            }
        }


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password1: str
    new_password2: str

    @field_validator('new_password1', 'new_password2')
    def password_length(cls, value: str):
        """Ensure password is at least 8 characters long."""
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return value

    @field_validator('new_password2')
    def passwords_match(cls, value, info: ValidationInfo):
        """Ensure both passwords match."""
        password1 = info.data["new_password1"]  # Use the new approach to get value
        if password1 is None or value != password1:
            raise ValueError('Passwords do not match')
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "old_password": "your-old-pwd",
                "new_password1": "your-new-pwd",
                "new_password2": "your-new-pwd",
            }
        }
