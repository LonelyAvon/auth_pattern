from datetime import datetime, timedelta, timezone
from uuid import UUID
from fastapi import Depends, HTTPException, Request, APIRouter, Response
from fastapi.security import HTTPBearer
from app.api.schemas.email import EmailCreate, EmailRead
from app.api.schemas.user import(
    UserCreate, 
    UserRead,
)
from app.api.schemas.token import Token
from app.db.models.models import User
from app.db.db import get_session
from app.db.repositories.user_repository.user_repo import UserRepository
from app.api.services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession
import app.api.authorization.utils.utils as utils
from .func import get_current_user, validate_current_user, refresh_acess_token
from app.api.services.email import EmailService

router = APIRouter(prefix="/user", tags=["User"])



@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, session: AsyncSession=Depends(get_session)):
    user: UserRead = await UserService(session).create(user)
    return user

@router.post("/login", response_model=Token)
async def login(response: Response, user: UserRead = Depends(validate_current_user)):
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role
    }
    access_token = utils.encode_jwt(payload=utils.create_token("access", jwt_payload))
    refresh_token = utils.encode_jwt(payload=utils.create_token("refresh", jwt_payload), expire_timedelta=timedelta(days=30))
    response.set_cookie("refresh_token", refresh_token, expires=datetime.now(timezone.utc) + timedelta(days=30), httponly=True, secure=True)
    return Token(access_token=access_token)

@router.get("/refresh", response_model=Token)
async def refresh(token: Token = Depends(refresh_acess_token)):
    return token

@router.get("/me", response_model=UserRead)
async def get(user: UserRead = Depends(get_current_user)):
    return user

@router.post('/email', response_model=EmailRead)
async def create_email(email: EmailCreate, session: AsyncSession=Depends(get_session)):
    email = await EmailService(session).create(email)
    return email