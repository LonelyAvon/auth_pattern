from fastapi import APIRouter

from .controllers import auth_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
