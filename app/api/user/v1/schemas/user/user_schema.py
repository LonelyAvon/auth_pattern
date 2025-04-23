from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    # model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    surname: str
    name: str
    patronymic: Optional[str] = None
    id_role: UUID
    is_archived: bool
