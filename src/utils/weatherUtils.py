###############################################################################################################
#    WeatherUtils.py   Copyright (C) <2026>  <Kevin Scott>                                                    #
#                                                                                                             #
#    Contains utility functions for generating weather data from openMeteo.com.                               #
#                                                                                                             #
###############################################################################################################
#                                                                                                             #
#    This program is free software: you can redistribute it and/or modify it under the terms of the           #
#    GNU General Public License as published by the Free Software Foundation, either Version 3 of the         #
#    License, or (at your option) any later Version.                                                          #
#                                                                                                             #
#    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without        #
#    even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#    GNU General Public License for more details.                                                             #
#                                                                                                             #
#    You should have received a copy of the GNU General Public License along with this program.               #
#    If not, see <http://www.gnu.org/licenses/>.                                                              #
#                                                                                                             #
###############################################################################################################

# pip install openmeteo-requests, requests_cache, retry_requests

import openmeteo_requests

import requests_cache
from retry_requests import retry

class Weather():

    def __init__(self, myConfig, myLogger):
        self.config = myConfig
        self.logger = myLogger

    def connect(self):
        #  Initialize session with caching and automated retries
        try:
            cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
            retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
            self.openmeteo = openmeteo_requests.Client(session=retry_session)
            self.logger.info(" Network connection to openMeteo.com successful.")
            return True
        except Exception as e:
            self.logger.error(f" Error initializing API client sessions: {e}")
            return False

    def getCurrentWeather(self):
        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
        "latitude": 53.743192,
        "longitude": -0.198817,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "wind_direction_10m", 
                    "wind_speed_10m", "wind_gusts_10m", "precipitation", "showers", "rain", "weather_code", "cloud_cover", 
                    "pressure_msl", "surface_pressure"],
        "timezone": "auto"}

        responses = self.openmeteo.weather_api(url, params = params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation: {response.Elevation()} m asl")
        print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

        # Process current data. The order of variables needs to be the same as requested.
        current = response.Current()
        current_temperature_2m = current.Variables(1).Value()
        current_relative_humidity_2m = current.Variables(2).Value()
        current_apparent_temperature = current.Variables(2).Value()
        current_is_day = current.Variables(3).Value()
        current_wind_direction_10m = current.Variables(4).Value()
        current_wind_speed_10m = current.Variables(5).Value()
        current_wind_gusts_10m = current.Variables(6).Value()
        current_precipitation = current.Variables(7).Value()
        current_showers = current.Variables(8).Value()
        current_rain = current.Variables(9).Value()
        current_weather_code = current.Variables(10).Value()
        current_cloud_cover = current.Variables(11).Value()
        current_pressure_msl = current.Variables(12).Value()
        current_surface_pressure = current.Variables(13).Value()

        print(f"\nCurrent time: {current.Time()}")
        print(f"Current temperature_2m: {current_temperature_2m}")
        print(f"Current relative_humidity_2m: {current_relative_humidity_2m}")
        print(f"Current apparent_temperature: {current_apparent_temperature}")
        print(f"Current is_day: {current_is_day}")
        print(f"Current wind_direction_10m: {current_wind_direction_10m}")
        print(f"Current wind_speed_10m: {current_wind_speed_10m}")
        print(f"Current wind_gusts_10m: {current_wind_gusts_10m}")
        print(f"Current precipitation: {current_precipitation}")
        print(f"Current showers: {current_showers}")
        print(f"Current rain: {current_rain}")
        print(f"Current weather_code: {current_weather_code}")
        print(f"Current cloud_cover: {current_cloud_cover}")
        print(f"Current pressure_msl: {current_pressure_msl}")
        print(f"Current surface_pressure: {current_surface_pressure}")

        return current

# Code	Description
# 0	Clear sky
# 1, 2, 3	Mainly clear, partly cloudy, and overcast
# 45, 48	Fog and depositing rime fog
# 51, 53, 55	Drizzle: Light, moderate, and dense intensity
# 56, 57	Freezing Drizzle: Light and dense intensity
# 61, 63, 65	Rain: Slight, moderate and heavy intensity
# 66, 67	Freezing Rain: Light and heavy intensity
# 71, 73, 75	Snow fall: Slight, moderate, and heavy intensity
# 77	Snow grains
# 80, 81, 82	Rain showers: Slight, moderate, and violent
# 85, 86	Snow showers slight and heavy
# 95 *	Thunderstorm: Slight or moderate
# 96, 99 *	Thunderstorm with slight and heavy hail