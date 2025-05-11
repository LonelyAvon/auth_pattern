from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.api.organization.models import Organization
from app.db import AbstractRepository


class OrganizationRepository(AbstractRepository):
    model = Organization

    async def get_organizations_with_users(self):
        query = select(self.model).options(joinedload(self.model.users))
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_organization_with_users(self, organization_id: UUID):
        query = (
            select(self.model)
            .options(joinedload(self.model.users))
            .where(self.model.id == organization_id)
        )
        result = await self._session.execute(query)
        return result.scalars().first()
