from typing import Optional

from pydantic import BaseModel


class UserUpdate(BaseModel):
    surname: Optional[str] = None
    name: Optional[str] = None
    patronymic: Optional[str] = None
