from app.db.repositories.user_repository.user_repo import UserRepository


class UserService:
    def __init__(self, session) :
        self.session = session

    async def get_sum(self):
        users = await UserRepository(self.session).get_all()
        answer = sum([user.sum for user in users])
        return answer