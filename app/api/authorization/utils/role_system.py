from fastapi import Depends, HTTPException, Request, status

from app.api.user.v1.schemas.user.user_read import UserRead
from app.api.user.v1.utils.auth.func import get_current_user
from app.settings import UserRoleEnum

# Декоратор для регистрации ролей


def roles_required(*required_roles: UserRoleEnum):
    async def check_roles(
        current_user: UserRead = Depends(get_current_user),
    ) -> UserRead:
        if UserRoleEnum.ANY in required_roles:
            return current_user
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user

    return check_roles
