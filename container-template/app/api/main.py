from fastapi import Depends, FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from app.settings import settings
from .routers import api_router
from sqlalchemy.exc import IntegrityError
from app.common.logger import logger

logger.critical("MESSAGE FROM LOGGER")

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



app.include_router(api_router)
