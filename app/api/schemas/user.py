from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class UserCreate(BaseModel):
    username: str
    password: str
    surname: str
    name: str
    patronymic: Optional[str] = None

class UserRead(BaseModel):
    id: UUID
    username: str
    surname: str
    name: str
    patronymic: Optional[str] = None
    role: Optional[str] = "user"
    is_archived: Optional[bool] = False


class UserUpdate(BaseModel):
    id: UUID = None
    username: Optional[str] = None
    password: Optional[str] = None
    surname: Optional[str] = None
    name: Optional[str] = None
    patronymic: Optional[str] = None
    is_archived: Optional[bool] = None

class UserAuthorization(BaseModel):
    username: str
    password: str