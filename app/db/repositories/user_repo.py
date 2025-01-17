from sqlalchemy import select
from app.db.repositories.abstract_repo import AbstractRepository

from app.db.models.models import User
from app.api.schemas.user import UserCreate
from app.api.authorization.utils import utils


class UserRepository(AbstractRepository):
    model =  User

    async def create(self, user: UserCreate):
        user.password = utils.hash_password(user.password)
        return await super().create(user)
    
    async def get_user_by_username(self, username: str):
        query = select(self.model).where(self.model.username == username)
        result = await self._session.execute(query)
        return result.scalars().first()