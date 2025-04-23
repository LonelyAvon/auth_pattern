from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from app.api.user.v1.utils.auth.utils import hash_password


class UserCreate(BaseModel):
    username: str
    password: bytes
    surname: str
    name: str
    id_role: UUID
    patronymic: Optional[str] = None

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, v):
        return hash_password(v)
