from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    surname: str
    name: str
    patronymic: Optional[str] = None
    role: str
    is_archived: bool
