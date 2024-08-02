from sqlite3 import IntegrityError
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from app.api.schemas.user import (
    UserRead,
    UserCreate
)
from app.db.db import get_session
from app.db.repositories.user_repository.user_repo import UserRepository
from app.settings import settings
from .routers import api_router
from sqlalchemy.exc import IntegrityError
from .authorization.func import get_current_user
from .authorization.google_oauth.main import authorization_url
from app.db.repositories.role_repo.role_repo import RoleRepository


app = FastAPI(
    title=settings.PROJECT_TITLE, 
    version="1.0.0",
    root_path=settings.FAST_API_PREFIX
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.exception_handler(IntegrityError)
async def integrity_error_handler(exc: IntegrityError):
    raise HTTPException(status_code=400, detail=str(exc.orig).split("\nDETAIL:  ")[1])


app.include_router(api_router)

@app.get("/GET", response_model=UserRead)
async def get(user: UserRead = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Acces denied")
    return user

@app.get("/redirect")
async def refirect():
    return RedirectResponse(authorization_url)