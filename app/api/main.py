from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware

from app.api.user.v1.utils.auth.func import get_current_user
from app.settings import settings

from .routers import api_router

app = FastAPI(
    title=settings.PROJECT_TITLE,
    version="1.0.0",
    root_path=settings.FAST_API_PREFIX,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
