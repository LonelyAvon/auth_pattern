from uuid import UUID

from fastapi import HTTPException, status

from app.api.organization.v1.repositories.organization import OrganizationRepository
from app.api.organization.v1.schemas.organization.create import OrganizationCreate
from app.api.organization.v1.schemas.organization.organization_read import (
    OrganizationRead,
)
from app.api.organization.v1.schemas.organization.organization_with_users import (
    OrganizationWithUsers,
)
from app.db import AsyncSession


class OrganizationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[OrganizationRead]:
        result = await OrganizationRepository(self.session).get_all()
        return result

    async def get_one(self, organization_id: UUID) -> OrganizationRead:
        result = await OrganizationRepository(self.session).get_by_id(organization_id)
        if result is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"Организация с id {organization_id} не найдена",
            )
        return result

    async def create(self, organization: OrganizationCreate) -> OrganizationRead:
        result = await OrganizationRepository(self.session).create(
            **organization.model_dump()
        )
        return result

    async def get_organizations_with_users(self) -> list[OrganizationWithUsers]:
        result = await OrganizationRepository(
            self.session
        ).get_organizations_with_users()
        return result

    async def get_organization_with_users(
        self, organization_id: UUID
    ) -> OrganizationWithUsers:
        result = await OrganizationRepository(self.session).get_organization_with_users(
            organization_id=organization_id
        )
        return result
