from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.api.user.v1.repositories import UserRepository
from app.api.user.v1.schemas import UserCreate, UserRead, UserSchema
from app.db import AsyncSession


class UserService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: UserCreate) -> UserSchema:
        try:
            result: UserSchema = await UserRepository(self._session).create(
                **user.model_dump()
            )
            return result
        except IntegrityError:
            raise HTTPException(status_code=400, detail="User already exists")

    async def get_user_by_username(self, username: str) -> UserSchema:
        result: UserSchema = await UserRepository(self._session).get_user_by_username(
            username
        )
        return result

    async def get_by_id(self, user_id: UUID) -> UserRead:
        result: UserSchema = await UserRepository(self._session).get_by_id(user_id)
        return result
