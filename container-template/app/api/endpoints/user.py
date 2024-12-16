from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.db.db import get_session
from app.db.repositories.user_repository.user_repo import UserRepository
from app.api.schemas.user import (
    UserCreate,
    UserUpdate, 
    User
)
from app.api.services.user import UserService

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("/get_all", response_model=list[User])
async def get_all(session=Depends(get_session)):
    users: list[User] = await UserRepository(session).get_all()
    return users

@router.get('/get_all_sum', response_model=float)
async def get_all_sum(session=Depends(get_session)):
    return await UserService(session).get_sum()

@router.get("/get_by_username", response_model=User)
async def get_user_by_username(username: str, session=Depends(get_session)):
    user: User = await UserRepository(session).get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/create", response_model=User)
async def create_user(user: UserCreate, session=Depends(get_session)):
    created_user: User = await UserRepository(session).create(user)
    await UserRepository(session).commit()
    return created_user

@router.put("/update/{id}", response_model=User)
async def update_user(id: UUID, user: UserUpdate, session=Depends(get_session)):
    updated_user: User = await UserRepository(session).update_one(id, user)
    await UserRepository(session).commit()
    return updated_user

@router.delete("/delete/{id}", response_model=int)
async def delete_user(id: UUID, session=Depends(get_session)):
    rows: int = await UserRepository(session).delete_by_id(id)
    await UserRepository(session).commit()
    return rows