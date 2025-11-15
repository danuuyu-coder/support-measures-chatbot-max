from os.path import dirname, abspath, join, exists

from aiofiles.os import mkdir
from aiosqlite import connect, Connection

class Database:
    def __init__(self):
        self._dir_path = join(dirname(abspath(__file__)), '..', '..', 'data')
        self._file_path = join(self._dir_path, 'database.sqlite')
        self._database: None | Connection = None

    async def __aenter__(self):
        if not exists(self._dir_path):
            await mkdir(self._dir_path)

        self._database = await connect(self._file_path)
        await self._database.execute('PRAGMA foreign_keys = ON')
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._database.commit()
        await self._database.close()

    async def execute(self, query: str, *params):
        await self._database.execute(query, params)

    async def select_one(self, query: str, *params):
        response = await self._database.execute(query, params)
        return await response.fetchone()

    async def select_all(self, query: str, *params):
        response = await self._database.execute(query, params)
        return await response.fetchall()
