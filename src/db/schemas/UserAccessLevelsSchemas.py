import uuid

from pydantic import BaseModel


class UserAccessLevelBaseSchema(BaseModel):
    role: str


class UserAccessLevelCreateSchema(UserAccessLevelBaseSchema):
    pass


class UserAccessLevelResponseSchema(UserAccessLevelBaseSchema):
    id: uuid.UUID


__all__ = [
    "UserAccessLevelBaseSchema",
    "UserAccessLevelCreateSchema",
    "UserAccessLevelResponseSchema"
]
