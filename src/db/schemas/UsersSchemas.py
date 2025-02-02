import re
import uuid
import email_validator

from datetime import datetime
from typing import Optional
from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=8, max_length=30)
    firstname: Optional[str] = Field(None, max_length=30)
    lastname: Optional[str] = Field(None, max_length=30)
    fatherhood: Optional[str] = Field(None, max_length=30)
    email: Optional[EmailStr] = None

    @field_validator("username")
    def validate_username(cls, value):
        if len(value) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Имя пользователя должно содержать не менее 8 символов."
            )

        if not re.match(r"^[a-zA-Z0-9]+$", value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Имя пользователя может содержать только буквы и цифры."
            )

        return value


class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=10, max_length=97)
    id_role: uuid.UUID

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пароль должен содержать не менее 10 символов."
            )

        if not re.search(r"[A-Za-z]", value) or not re.search(r"\d", value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пароль должен содержать хотя бы одну букву и цифру."
            )

        return value

    @field_validator("email")
    def validate_email(cls, value):
        if value is not None and value != "":
            try:
                email_validator.validate_email(value)

                return value

            except email_validator.EmailNotValidError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Неверный формат email"
                )


class UserResponseSchema(UserBaseSchema):
    id: uuid.UUID
    created_at: datetime


__all__ = [
    "UserCreateSchema",
    "UserResponseSchema",
    "UserBaseSchema"
]
