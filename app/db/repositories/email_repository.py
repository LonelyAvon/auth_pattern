from .abstract_repo import AbstractRepository
from app.db.models.models import Email

class EmailRepository(AbstractRepository):
    model = Email