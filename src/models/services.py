from src.services import UserService, RegionService, MeasureService, GeoService, GigaService


class Services:
    def __init__(
            self,
            user_service: UserService,
            region_service: RegionService,
            measure_service: MeasureService,
            geo_service: GeoService,
            giga_service: GigaService
    ):
        self.user_service = user_service
        self.region_service = region_service
        self.measure_service = measure_service
        self.geo_service = geo_service
        self.giga_service = giga_service
