from fastapi import APIRouter

from .controllers import role_router

router = APIRouter(prefix="/v1")

router.include_router(role_router)
