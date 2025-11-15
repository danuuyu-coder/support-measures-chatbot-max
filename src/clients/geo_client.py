from aiohttp import ClientSession

class GeoClient:
    def __init__(self, token: str):
        self._url_base = f'https://geocode-maps.yandex.ru/v1?apikey={token}'

    async def fetch(self, longitude: float, latitude: float):
        url = f'{self._url_base}&geocode={longitude},{latitude}&lang=ru_RU&format=json'
        async with ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
