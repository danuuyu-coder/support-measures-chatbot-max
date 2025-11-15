from src.clients.fetcher import Fetcher

class MeasureClient:
    def __init__(self, fetcher: Fetcher):
        self._fetcher = fetcher
        self._filename = lambda okato: f'{okato}.json'
        self._filename_military = lambda okato: f'military_{okato}.json'
        self._url = 'https://www.gosuslugi.ru/api/nsi/v1/dictionary/FZO_mery_podderjki'
        self._url_military = 'https://www.gosuslugi.ru/api/nsi/v1/dictionary/FZO_mery_podderjki_military'
        self._data = lambda okato: {
            'treeFiltering': 'ONELEVEL',
            'pageNum': 1,
            'pageSize': 5000,
            'parentRefItemValue': '',
            'selectAttributes': [
                '*',
            ],
            'orderBy': [
                {
                    'attributeName': 'Uroven_mery_podderjki',
                    'sortDirection': 'ASC',
                },
            ],
            'filter': {
                'union': {
                    'unionKind': 'AND',
                    'subs': [
                        {
                            'union': {
                                'unionKind': 'OR',
                                'subs': [
                                    {
                                        'simple': {
                                            'attributeName': 'OKATO',
                                            'condition': 'EQUALS',
                                            'value': {
                                                'asString': okato,
                                            },
                                        },
                                    },
                                    {
                                        'simple': {
                                            'attributeName': 'OKATO',
                                            'condition': 'EQUALS',
                                            'value': {
                                                'asString': '',
                                            },
                                        },
                                    },
                                ],
                            },
                        },
                    ],
                },
            },
        }
        self._data_military = lambda okato: {"treeFiltering":"ONELEVEL","pageNum":1,"pageSize":5000,"parentRefItemValue":"","selectAttributes":["*"],"orderBy":[{"attributeName":"Uroven_mery_podderjki","sortDirection":"ASC"}],"filter":{"union":{"unionKind":"AND","subs":[{"union":{"unionKind":"OR","subs":[{"simple":{"attributeName":"OKATO","condition":"EQUALS","value":{"asString":okato}}},{"simple":{"attributeName":"OKATO","condition":"EQUALS","value":{"asString":""}}}]}}]}}}

    async def fetch(self, okato: str):
        return await self._fetcher.fetch(
            self._filename(okato),
            self._url,
            self._data(okato)
        )

    async def fetch_military(self, okato: str):
        return await self._fetcher.fetch(
            self._filename_military(okato),
            self._url_military,
            self._data_military(okato)
        )
