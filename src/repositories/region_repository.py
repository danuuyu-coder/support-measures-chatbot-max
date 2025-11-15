from src.repositories.database import Database
from src.models import Region

class RegionRepository:
    def __init__(self, database: Database):
        self._database = database

    async def create_table(self):
        await self._database.execute('''
            CREATE TABLE IF NOT EXISTS regions (
                okato TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')

    async def insert(self, region: Region):
        await self._database.execute('''
            INSERT OR REPLACE INTO regions (okato, name)
                VALUES (?, ?)
        ''', *region.tuple())

    async def get_one(self, name: str):
        region_tuple = await self._database.select_one('''
            SELECT * FROM regions WHERE name = ?
        ''', name)
        return None if region_tuple is None else Region(*region_tuple)

    async def get_all(self):
        region_tuples = await self._database.select_all('''
            SELECT * FROM regions
        ''')
        regions = [Region(*region_tuple) for region_tuple in region_tuples]
        return regions
