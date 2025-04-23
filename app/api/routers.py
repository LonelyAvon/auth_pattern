from fastapi.routing import APIRouter

from app.api.roles.router import router as roles
from app.api.user.router import router as user

# from .authorization import auto

api_router = APIRouter()
api_router.include_router(user)
api_router.include_router(roles)
