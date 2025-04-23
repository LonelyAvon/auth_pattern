from uuid import UUID

from pydantic import BaseModel


class RoleRead(BaseModel):
    id: UUID
    name: str
