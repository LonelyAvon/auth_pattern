from fastapi import HTTPException
from app.api.schemas.user import UserCreate
from app.db.models.models import User
from app.db.repositories.user_repository.user_repo import UserRepository
from .email import is_valid_email


class UserService:
    def __init__(self, session) :
        self.session = session

    async def get_sum(self):
        users = await UserRepository(self.session).get_all()
        answer = sum([user.sum for user in users])
        return answer
    
    async def create(self, user: UserCreate):
        find_user: User = await UserRepository(self.session).get_user_by_username(user.username)
        if find_user:
            raise HTTPException(status_code=400, detail="User already exists")
        # if not is_valid_email(user.username):
        #     raise HTTPException(status_code=400, detail="Invalid email")
        user = await UserRepository(self.session).create(user)
        await UserRepository(self.session).commit()
        return user