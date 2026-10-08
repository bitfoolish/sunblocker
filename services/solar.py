import numpy as np
import pandas as pd
from pvlib.location import Location

## The period in which the sun is shining
class SolarWindow:
    def __init__(self, lat: float, long: float, orientation: float, tz: str = "UTC"):
        self.location = Location(latitude=lat, longitude=long, tz=tz)
        self.orientation = orientation ## compase direction window is facing
    
    def is_sun_shining(self, time: pd.Timestamp) -> bool:
        solpos = self.location.get_solarposition(time)
        elev = solpos['elevation'].iloc[0]
        return elev > 0 # sun is above horizon

    def is_sun_facing_window(self, time: pd.Timestamp, fov: float = 90.0) -> bool:
        solpos = self.location.get_solarposition(time)
        sun_azimuth = solpos['azimuth'].iloc[0]
        sun_elev = solpos['elevation'].iloc[0]

        if sun_elev <= 0:
            return False

        angle_diff = abs(sun_azimuth - self.orientation)
        is_within_fov = angle_diff <= (fov / 2)
        return is_within_fov
        

# site = Location(latitude=53.360001, longitude=-6.325000, tz="Europe/Dublin")

s = SolarWindow(53.360001, -6.325000, 180, "Europe/Dublin")
current_time = pd.Timestamp.now(tz="Europe/Dublin")

# print(s.is_sun_shining(current_time))
print(s.is_sun_facing_window(current_time, 50))