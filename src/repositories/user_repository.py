from src.repositories.database import Database
from src.models import User

class UserRepository:
    def __init__(self, database: Database):
        self._database = database

    async def create_table(self):
        await self._database.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                okato TEXT NOT NULL,
                FOREIGN KEY (okato) REFERENCES regions(okato)
            )
        ''')

    async def insert(self, user: User):
        await self._database.execute('''
            INSERT OR REPLACE INTO users (user_id, okato)
                VALUES (?, ?)
        ''', *user.tuple())

    async def remove(self, user_id: int):
        await self._database.execute('''
            DELETE FROM users WHERE user_id = ?
        ''', user_id)

    async def get_one(self, user_id: int):
        user_tuple = await self._database.select_one('''
            SELECT * FROM users WHERE user_id = ?
        ''', user_id)
        return None if user_tuple is None else User(*user_tuple)
