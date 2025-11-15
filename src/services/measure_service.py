from typing import List

from src.clients import MeasureClient
from src.models import Measure
from src.repositories import MeasureRepository
from src.services import RegionService

class MeasureService:
    def __init__(
            self,
            measure_repository: MeasureRepository,
            measure_client: MeasureClient,
            region_service: RegionService
    ):
        self._measure_repository = measure_repository
        self._measure_client = measure_client
        self._region_service = region_service

    async def update(self):
        await self._measure_repository.create_table()
        regions = await self._region_service.get_all()
        for region in regions:
            measures = await self.parse(region.okato, False)
            for measure in measures:
                await self._measure_repository.insert(measure)

            measures = await self.parse(region.okato, True)
            for measure in measures:
                await self._measure_repository.insert_military(measure)

    async def parse(self, okato, is_military: bool):
        measures = []
        if is_military:
            response = await self._measure_client.fetch(okato)
        else:
            response = await self._measure_client.fetch_military(okato)

        for item in response['items']:
            link = item['attributeValues']['Ssylka_na_uslugu'] if 'Ssylka_na_uslugu' in item['attributeValues'] else None
            docs = item['attributeValues']['Doc_dlya_polucheniya_1'] if 'Doc_dlya_polucheniya_1' in item['attributeValues'] else None
            dur = item['attributeValues']['Srok_okazaniya'] if 'Srok_okazaniya' in item['attributeValues'] else None
            order = item['attributeValues']['Poryadok_deystviy'] if 'Poryadok_deystviy' in item['attributeValues'] else None
            res = item['attributeValues']['Result'] if 'Result' in item['attributeValues'] else None
            measure = Measure(
                item['attributeValues']['ID_Mera_podderjki'],
                okato,
                item['title'],
                dur,
                docs,
                order,
                res,
                link
            )
            measures.append(measure)
        return measures

    async def get_all(self, okato):
        return await self._measure_repository.get_all(okato)

    async def get_all_military(self, okato):
        return await self._measure_repository.get_all_military(okato)

    async def get_one(self, measure_id: str):
        return await self._measure_repository.get_one(measure_id)

    async def get_one_military(self, measure_id: str):
        return await self._measure_repository.get_one_military(measure_id)
