
from uuid import UUID
from pydantic import BaseModel
from typing import Optional



class User(BaseModel):
    id: UUID
    username: str
    store_id: Optional[UUID] = None
    is_active: bool
    sum: Optional[float] = None

class UserCreate(BaseModel):
    username: str
    store_id: Optional[UUID] = None
    is_active: Optional[bool] = False
    sum: Optional[float] = 0

class UserUpdate(BaseModel):
    username: Optional[str] = None
    sum: Optional[float] = 10