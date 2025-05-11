from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.authorization.utils.role_system import roles_required
from app.api.organization.v1.schemas.organization.create import OrganizationCreate
from app.api.organization.v1.schemas.organization.organization_read import (
    OrganizationRead,
)
from app.api.organization.v1.schemas.organization.organization_with_users import (
    OrganizationWithUsers,
)
from app.api.organization.v1.services.organization import OrganizationService
from app.api.user.v1.utils.auth.func import CurrentUserDep
from app.db import AsyncSessionDep
from app.settings import UserRoleEnum

router = APIRouter(
    prefix="/organization",
    tags=["Организации"],
    dependencies=[Depends(roles_required(UserRoleEnum.ADMIN))],
)


@router.get("/all", response_model=List[OrganizationRead])
async def get_all(
    session: AsyncSessionDep,
):
    result = await OrganizationService(session).get_all()
    return result


@router.get(
    "/{organization_id}",
    response_model=OrganizationRead,
)
async def get_organization(
    organization_id: UUID,
    session: AsyncSessionDep,
):
    result: OrganizationRead = await OrganizationService(session).get_one(
        organization_id
    )
    return result


@router.get(
    "/all/users",
    response_model=List[OrganizationWithUsers],
)
async def get_all_with_users(session: AsyncSessionDep):
    result = await OrganizationService(session).get_organizations_with_users()

    return result


@router.get(
    "/{organization_id}/users",
    response_model=OrganizationWithUsers,
)
async def get_one_with_users(organization_id: UUID, session: AsyncSessionDep):
    result = await OrganizationService(session).get_organization_with_users(
        organization_id
    )
    return result


@router.post(
    "/create",
    response_model=OrganizationRead,
)
async def create(
    organization: OrganizationCreate,
    session: AsyncSessionDep,
):
    result = await OrganizationService(session).create(organization)
    return result
