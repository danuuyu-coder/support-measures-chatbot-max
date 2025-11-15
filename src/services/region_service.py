from src.clients import RegionClient
from src.models import Region
from src.repositories import RegionRepository

class RegionService:
    def __init__(self, region_repository: RegionRepository, region_client: RegionClient):
        self._region_repository = region_repository
        self._region_client = region_client

    async def update(self):
        regions = await self.parse()
        await self._region_repository.create_table()
        for region in regions:
            await self._region_repository.insert(region)

    async def parse(self):
        regions = []
        response = await self._region_client.fetch()
        for item in response['items']:
            region = Region(item['attributeValues']['OKATO'], item['title'])
            regions.append(region)
        return regions

    async def get_one(self, name: str):
        return await self._region_repository.get_one(name)

    async def get_all(self):
        return await self._region_repository.get_all()
