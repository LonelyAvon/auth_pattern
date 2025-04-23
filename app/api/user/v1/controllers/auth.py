from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import HTTPBearer

from app.api.authorization.utils.role_system import roles_required
from app.api.user.v1.schemas import Token, UserCreate, UserRead, UserSchema
from app.api.user.v1.services.user import UserService
from app.api.user.v1.utils.auth.func import CurrentUserDep, validate_current_user
from app.api.user.v1.utils.auth.utils import create_token, encode_jwt
from app.db import AsyncSessionDep
from app.settings import UserRoleEnum

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)


@router.post(
    "/register",
    response_model=UserSchema,
    dependencies=[
        Depends(
            roles_required(
                UserRoleEnum.ADMIN,
                UserRoleEnum.USER,
            )
        ),
    ],
)
async def register(
    user: UserCreate,
    current_user: CurrentUserDep,
    session: AsyncSessionDep,
):
    user = await UserService(session).create(user)
    return user


@router.post("/login", response_model=Token)
async def login(response: Response, user: UserRead = Depends(validate_current_user)):
    jwt_payload = {"sub": str(user.id), "username": user.username, "role": user.role}
    access_token = encode_jwt(payload=create_token("access", jwt_payload))
    refresh_token = encode_jwt(
        payload=create_token("refresh", jwt_payload),
        expire_timedelta=timedelta(days=30),
    )

    response.set_cookie(
        "refresh_token",
        refresh_token,
        expires=datetime.now(timezone.utc) + timedelta(days=30),
        httponly=True,
        secure=True,
    )
    return Token(access_token=access_token)


# # @router.get("/refresh", response_model=Token)
# # async def refresh(token: Token = Depends(refresh_acess_token)):
# #     return token


@router.get(
    "/users/me",
    response_model=UserRead,
    dependencies=[Depends(roles_required(UserRoleEnum.ANY))],
)
async def me(current_user: CurrentUserDep):
    return current_user
