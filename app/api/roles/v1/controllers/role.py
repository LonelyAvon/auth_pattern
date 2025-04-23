from typing import List

from fastapi import APIRouter, Depends

from app.api.authorization.utils.role_system import roles_required
from app.api.roles.v1.schemas import RoleCreate, RoleRead
from app.api.roles.v1.services import RoleService
from app.api.user.v1.utils.auth.func import CurrentUserDep
from app.db import AsyncSessionDep
from app.settings import UserRoleEnum

router = APIRouter(
    prefix="/roles",
    tags=["Роли"],
    dependencies=[Depends(roles_required(UserRoleEnum.ADMIN))],
)


@router.get(
    "/all",
    response_model=List[RoleRead],
)
async def get_all(
    session: AsyncSessionDep,
) -> List[RoleRead]:
    roles: List[RoleRead] = await RoleService(session).get_all()
    return roles


@router.post(
    "/create",
    response_model=RoleRead,
)
async def create(
    role: RoleCreate,
    session: AsyncSessionDep,
):
    role: RoleRead = await RoleService(session).create(role)
    return role
