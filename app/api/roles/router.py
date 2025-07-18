from fastapi import APIRouter

from .v1.router import router as v1_role_router

router = APIRouter()

router.include_router(v1_role_router)
