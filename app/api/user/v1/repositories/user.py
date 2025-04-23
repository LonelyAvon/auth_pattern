from uuid import UUID

from sqlalchemy import select

from app.api.roles.models import Role
from app.api.user.models import User
from app.db import AbstractRepository


class UserRepository(AbstractRepository):
    model = User

    async def get_user_by_username(self, username: str):
        query = select(self.model).where(self.model.username == username)
        result = await self._session.execute(query)
        return result.scalars().first()

    async def get_by_id(self, user_id: UUID):
        query = (
            select(
                self.model.id,
                self.model.username,
                self.model.surname,
                self.model.name,
                self.model.patronymic,
                self.model.is_archived,
                Role.name.label("role"),
            )
            .where(self.model.id == user_id)
            .join(self.model.role)
        )
        result = await self._session.execute(query)
        return result.mappings().first()
