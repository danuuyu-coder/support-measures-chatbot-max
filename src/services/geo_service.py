from src.clients.geo_client import GeoClient

class GeoService:
    def __init__(self, geo_client: GeoClient):
        self._geo_client = geo_client

    async def parse(self, longitude: float, latitude: float):
        data = await self._geo_client.fetch(longitude, latitude)
        first_result = data['response']['GeoObjectCollection']['featureMember'][0]
        region = first_result['GeoObject']['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName']
        country = first_result['GeoObject']['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['CountryName']
        return region, country
