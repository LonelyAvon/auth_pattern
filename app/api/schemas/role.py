from uuid import UUID
from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str

class Role(BaseModel):
    id: UUID
    name: str

class RoleRead(Role):
    pass