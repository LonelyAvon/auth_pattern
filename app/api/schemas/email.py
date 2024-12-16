from uuid import UUID
from pydantic import BaseModel



class EmailCreate(BaseModel):
    email: str
    name: str
    type: str

class EmailRead(BaseModel):
    id: UUID
    email: str
    name: str
    type: str