import numpy as np
import pandas as pd
from pvlib.location import Location

## The period in which the sun is shining
class SolarWindow:
    def __init__(self, lat: float, long: float, orientation: float, tz: str = "UTC"):
        self.location = Location(latitude=lat, longitude=long, tz=tz)
        self.orientation = orientation ## compase direction window is facing
    
    def _get_solar_data(self, time: pd.Timestamp):
        solpos = self.location.get_solarposition(time)
        return (solpos['elevation'].iloc[0], solpos['azimuth'].iloc[0])

    def is_sun_shining(self, time: pd.Timestamp) -> bool:
        sun_elev, _ = self._get_solar_data(time)
        return sun_elev > 0 # sun is above horizon

    def is_sun_facing_window(self, time: pd.Timestamp, fov: float = 90.0) -> bool:
        elev, sun_azimuth = self._get_solar_data(time)

        if elev <= 0: # sun is at/below horizon
            return False

        angle_diff = abs((sun_azimuth - self.orientation + 180) % 360 - 180)
        is_within_fov = angle_diff <= (fov / 2)
        return is_within_fov

    ## Is sun elevated enough to glare
    def is_elevated_enough(self, time: pd.Timestamp) -> bool:
        sun_elev, _ = self._get_solar_data(time)
        is_within_elev = 5 <= sun_elev <= 45
        return is_within_elev
    
    def is_geometric_glare(self, time: pd.Timestamp, fov: float = 90.0, min_elev: float = 5.0, max_elev: float = 45.0) -> bool:
        elev, sun_azimuth = self._get_solar_data(time)

        if not (min_elev <= elev <= max_elev):
            return False

        angle_diff = abs((sun_azimuth - self.orientation + 180) % 360 - 180)
        return angle_diff <= (fov / 2)

        # return self.is_sun_facing_window(time, fov) and self.is_elevated_enough(time)

# site = Location(latitude=53.360001, longitude=-6.325000, tz="Europe/Dublin")

# s = SolarWindow(53.360001, -6.325000, 180, "Europe/Dublin")
# current_time = pd.Timestamp.now(tz="Europe/Dublin")

# print(s.is_sun_shining(current_time))
# print(s.is_sun_facing_window(current_time, 50))



# Instantiate South-Facing Window in Dublin (180° orientation)
south_window = SolarWindow(53.360001, -6.325000, 180, tz="Europe/Dublin")

''' -----------------------------------------------------------------------------
# Test Cases 
## 1. Noon in Summer
## 2. Nighttime
## 3. Current
----------------------------------------------------------------------------- '''

# Case 2: Noon time in Summer
t_summer_noon = pd.Timestamp("2026-06-21 13:00:00", tz="Europe/Dublin")

print("\n--- Case 2: Summer Noon (High Elevation) ---")
print(
    f"Is Facing Window?     {south_window.is_sun_facing_window(t_summer_noon, fov=90)}"
)  # True
print(
    f"Is Geometric Glare?   {south_window.is_geometric_glare(t_summer_noon, fov=90)}"
)  # False (Elevation too high)


# Case 2: Night time
t_night = pd.Timestamp("2026-10-15 22:00:00", tz="Europe/Dublin")

print("\n--- Case 3: Night Time ---")
print(f"Is Sun Shining?       {south_window.is_sun_shining(t_night)}")  # False
print(
    f"Is Geometric Glare?   {south_window.is_geometric_glare(t_night, fov=90)}"
)  # False

# Case 3: Current time
print("\n--- Case 3: Current Time ---")
print(f"Is Sun Shining?       {south_window.is_sun_shining(current_time)}")
print(f"Is Geometric Glare?   {south_window.is_geometric_glare(current_time, fov=90)}")  