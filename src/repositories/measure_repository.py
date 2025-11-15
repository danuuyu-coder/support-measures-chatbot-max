from src.repositories.database import Database
from src.models import Measure


class MeasureRepository:
    def __init__(self, database: Database):
        self._database = database

    async def create_table(self):
        await self._database.execute('''
            CREATE TABLE IF NOT EXISTS measures (
                measure_id TEXT PRIMARY KEY,
                okato TEXT NOT NULL,
                name TEXT NOT NULL,
                duration TEXT,
                documents TEXT,
                procedure TEXT,
                result TEXT,
                link TEXT
            )
        ''')

        await self._database.execute('''
            CREATE TABLE IF NOT EXISTS military_measures (
                measure_id TEXT PRIMARY KEY,
                okato TEXT NOT NULL,
                name TEXT NOT NULL,
                duration TEXT,
                documents TEXT,
                procedure TEXT,
                result TEXT,
                link TEXT
            )
        ''')

    async def insert(self, measure: Measure):
        await self._database.execute('''
            INSERT OR REPLACE INTO measures (measure_id, okato, name, duration, documents, procedure, result, link)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', *measure.tuple())

    async def insert_military(self, measure: Measure):
        await self._database.execute('''
            INSERT OR REPLACE INTO military_measures (measure_id, okato, name, duration, documents, procedure, result, link)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', *measure.tuple())

    async def get_all(self, okato: str):
        measure_tuples = await self._database.select_all('''
             SELECT * FROM measures WHERE okato = ?
         ''', okato)
        measures = [Measure(*measure_tuple) for measure_tuple in measure_tuples]
        return measures

    async def get_all_military(self, okato: str):
        measure_tuples = await self._database.select_all('''
             SELECT * FROM military_measures WHERE okato = ?
         ''', okato)
        measures = [Measure(*measure_tuple) for measure_tuple in measure_tuples]
        return measures

    async def get_one(self, measure_id: str):
        measure_tuple = await self._database.select_one('''
             SELECT * FROM measures WHERE measure_id = ?
         ''', measure_id)
        return None if measure_tuple is None else Measure(*measure_tuple)

    async def get_one_military(self, measure_id: str):
        measure_tuple = await self._database.select_one('''
             SELECT * FROM military_measures WHERE measure_id = ?
         ''', measure_id)
        return None if measure_tuple is None else Measure(*measure_tuple)