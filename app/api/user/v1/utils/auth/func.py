import re

from fastapi import Depends, Form, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer
from typing_extensions import Annotated

from app.api.user.v1.repositories.user import UserRepository
from app.api.user.v1.schemas import Token, UserRead
from app.api.user.v1.services.user import UserService
from app.db import get_session
from app.settings import settings

from .utils import create_token, decode_jwt, encode_jwt, validate_password


async def get_current_user(
    request: Request,
    access_token: HTTPAuthorizationCredentials = Depends(
        OAuth2PasswordBearer(tokenUrl=f"{settings.FAST_API_PREFIX}/v1/auth/login")
    ),
):
    decoded: dict = decode_jwt(access_token)
    if decoded.get("token_type") is None:
        raise HTTPException(status_code=401, detail="Invalid token type")
    if decoded["token_type"] != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")
    async for session in get_session():
        user: UserRead = await UserService(session).get_by_id(decoded["sub"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_archived:
            raise HTTPException(status_code=401, detail="User is archived")

        request.state.current_user = user

        return user


async def validate_current_user(username: str = Form(), password: str = Form()):
    async for session in get_session():
        user = await UserService(session).get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not validate_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        if user.is_archived:
            raise HTTPException(status_code=401, detail="User is archived")
        return user


async def refresh_acess_token(request: Request):
    cookies = request.cookies
    refresh_token = cookies.get("refresh_token", None)
    if refresh_token is None:
        raise HTTPException(status_code=403, detail="Access denied")

    decoded = decode_jwt(refresh_token)
    if decoded.get("token_type", None) is None:
        raise HTTPException(status_code=401, detail="Invalid token type")
    if decoded["token_type"] != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    async for session in get_session():
        user: UserRead = await UserRepository(session).get_by_id(decoded["sub"])
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        if user.is_archived:
            raise HTTPException(status_code=401, detail="User is archived")
        jwt_payload = {
            "sub": str(user.id),
            "username": user.username,
            "role": user.role,
        }
        access_token = encode_jwt(payload=create_token("access", jwt_payload))
        return Token(access_token=access_token)


async def get_current_user_request(request: Request):
    # try:
    return request.state.current_user


CurrentUserDep = Annotated[UserRead, Depends(get_current_user_request)]
