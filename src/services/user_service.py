from src.models import User
from src.repositories import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def update(self):
        await self._user_repository.create_table()

    async def insert(self, user: User):
        await self._user_repository.insert(user)

    async def remove(self, user_id: int):
        await self._user_repository.remove(user_id)

    async def get_one(self, user_id: int):
        return await self._user_repository.get_one(user_id)
