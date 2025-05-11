from uuid import UUID

from pydantic import BaseModel


class OrganizationRead(BaseModel):
    id: UUID
    name: str
