from fastapi import APIRouter

from .controllers.organization import router as organization_router

router = APIRouter(prefix="/v1")


router.include_router(organization_router)
