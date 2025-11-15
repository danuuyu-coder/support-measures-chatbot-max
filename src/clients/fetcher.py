from json import loads, dumps
from os.path import dirname, abspath, join, exists
from typing import Dict, Any

from aiofiles import open
from aiofiles.os import remove, listdir, mkdir
from aiohttp import ClientSession

class Fetcher:
    def __init__(self):
        self._cache_path = join(dirname(abspath(__file__)), '..', '..', 'cache')
        self._session = None

    async def get_session(self):
        if self._session is None:
            self._session = ClientSession()
        return self._session
    
    async def fetch(self, filename: str, url: str, data: Dict[str, Any]):
        if self.file_is_exists(filename):
            return loads(await self.read_file(filename))

        session = await self.get_session()
        async with session.post(url, json=data) as response:
            response.raise_for_status()
            text = dumps(await response.json(), ensure_ascii=False, indent=2)
            await self.write_file(filename, text)
            return await response.json()

    async def read_file(self, filename: str):
        file_path = join(self._cache_path, filename)
        async with open(file_path, 'r', encoding='utf-8') as file:
            return await file.read()

    async def write_file(self, filename: str, data: str):
        if not exists(self._cache_path):
            await mkdir(self._cache_path)

        file_path = join(self._cache_path, filename)
        async with open(file_path, 'w', encoding='utf-8') as file:
            await file.write(data)

    async def clear(self):
        filenames = await listdir(self._cache_path)
        for filename in filenames:
            file_path = join(self._cache_path, filename)
            await remove(file_path)

    def file_is_exists(self, filename: str):
        file_path = join(self._cache_path, filename)
        return exists(file_path)
