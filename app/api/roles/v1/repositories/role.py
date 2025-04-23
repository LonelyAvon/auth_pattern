from app.api.roles.models import Role
from app.db import AbstractRepository


class RoleRepository(AbstractRepository):
    model = Role
