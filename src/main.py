import asyncio

from src.models import Services, Settings
from src.repositories import Database, UserRepository, RegionRepository, MeasureRepository
from src.clients import Fetcher, RegionClient, MeasureClient, GeoClient, GigaClient
from src.services import UserService, RegionService, MeasureService, GeoService, GigaService
from src.bot.middlewares import DIMiddleware, ErrorMiddleware
from src.bot import App

import logging 

async def main():
    settings = Settings()

    database = Database()
    user_repository = UserRepository(database)
    region_repository = RegionRepository(database)
    measure_repository = MeasureRepository(database)

    fetcher = Fetcher()
    region_client = RegionClient(fetcher)
    measure_client = MeasureClient(fetcher)
    geo_client = GeoClient(settings.yandex_token)
    giga_client = GigaClient(settings.giga_token)

    user_service = UserService(user_repository)
    region_service = RegionService(region_repository, region_client)
    measure_service = MeasureService(measure_repository, measure_client, region_service)
    geo_service = GeoService(geo_client)
    giga_service = GigaService(giga_client, region_repository, measure_repository)

    services = Services(user_service, region_service, measure_service, geo_service, giga_service)
    di_middleware = DIMiddleware(services)
    error_middleware = ErrorMiddleware()
    app = App(settings.max_token, error_middleware, di_middleware)

    async with database:
        await user_service.update()
        await region_service.update()
        await measure_service.update()

        await app.run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    asyncio.run(main())
