from src.clients.fetcher import Fetcher

class RegionClient:
    def __init__(self, fetcher: Fetcher):
        self._fetcher = fetcher
        self._filename = 'regions.json'
        self._url = 'https://www.gosuslugi.ru/api/nsi/v1/dictionary/FZO_regions_okato'
        self._data = {
            'treeFiltering':'ONELEVEL',
            'pageNum':1,
            'pageSize':255,
            'parentRefItemValue':'',
            'selectAttributes':['*']
        }

    async def fetch(self):
        return await self._fetcher.fetch(
            self._filename,
            self._url,
            self._data
        )
