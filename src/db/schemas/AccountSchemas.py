import uuid

from pydantic import BaseModel


class AccountBaseSchema(BaseModel):
    balance: float


class AccountCreateSchema(AccountBaseSchema):
    id_user: uuid.UUID


class AccountResponseSchema(AccountBaseSchema):
    id: uuid.UUID
    id_user: uuid.UUID


__all__ = [
    "AccountBaseSchema",
    "AccountCreateSchema",
    "AccountResponseSchema"
]
