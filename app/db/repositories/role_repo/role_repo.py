from app.db.repositories.abstract_repo import AbstractRepository
from app.db.models.models import Role


class RoleRepository(AbstractRepository):
    model =  Role