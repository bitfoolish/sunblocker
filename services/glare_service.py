import pandas as pd
from services.solar_service import SolarWindow
from services.weather_service import WeatherService

class GlareEvaluatorService:
    def __init__(self, weather_service: WeatherService = WeatherService()):
        self.weather_service = weather_service

    async def evaluate_glare(
        self, lat: float, lon: float, orientation: float, tz: str, time: pd.Timestamp, fov: float = 90.0) -> dict:
        window = SolarWindow(lat=lat, lon=lon, orientation=orientation, tz=tz)

        # Check solar glare first        
        geometric_glare = window.is_geometric_glare(time, fov=fov)
        
        if not geometric_glare:
            return {
                "has_glare": False,
                "reason": "Geometry out of bounds",
                "cloud_cover_pct": None
            }

        # Check for clouds
        pass 