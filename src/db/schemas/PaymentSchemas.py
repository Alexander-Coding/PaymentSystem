import uuid

from pydantic import BaseModel, Field


class PaymentBaseSchema(BaseModel):
    amount: float
    signature: str = Field(..., min_length=64, max_length=64)


class PaymentCreateSchema(PaymentBaseSchema):
    id_user: uuid.UUID
    id_account: uuid.UUID


class PaymentResponseSchema(PaymentBaseSchema):
    id: uuid.UUID
    id_user: uuid.UUID
    id_account: uuid.UUID


__all__ = [
    "PaymentBaseSchema",
    "PaymentCreateSchema",
    "PaymentResponseSchema"
]
