from typing import List

from app.api.roles.v1.repositories import RoleRepository
from app.api.roles.v1.schemas import RoleCreate, RoleRead
from app.db import AsyncSession


class RoleService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[RoleRead]:
        return await RoleRepository(self.session).get_all()

    async def create(self, role: RoleCreate) -> RoleRead:
        return await RoleRepository(self.session).create(**role.model_dump())
