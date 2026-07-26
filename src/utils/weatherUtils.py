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

import requests
import requests_cache
from retry_requests import retry

class Weather():

    def __init__(self, myConfig, myLogger):
        self.config = myConfig
        self.logger = myLogger

    def connect(self):
        # #  Initialize session with caching and automated retries
        # try:
        #     cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
        #     retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        #     self.openmeteo = openmeteo_requests.Client(session=retry_session)
        #     self.logger.info(" Network connection to openMeteo.com successful.")
        #     return True
        # except Exception as e:
        #     self.logger.error(f" Error initializing API client sessions: {e}")
        #     return False
        #  Initialize session with caching and automated retries

        #  Initialize without session with caching and automated retries
        try:
            self.openmeteo = openmeteo_requests.Client()
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

        #  Execute the API Request with network exception handling
        try:
            responses = self.openmeteo.weather_api(url, params=params)
            
            if not responses:
                self.logger.error("Error: Received an empty response array from the API.")
                return None
                
            response = responses[0]
            self.logger.debug(f"Fetching data from Open-Meteo for Lat: {response.Latitude()}, Lon: {response.Longitude()}")
                        
        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f"HTTP error occurred (Check coordinates or parameters): {http_err}")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            self.logger.error(f"Network connection error occurred: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            self.logger.error(f"The request timed out: {timeout_err}")
            return None
        except Exception as err:
            self.logger.error(f"An unexpected API error occurred: {err}")
            return None

        return responses[0]


    def degreesToText(self, degrees):
        """  Normalise degrees to be between 0 and 360
        """
        degrees = degrees % 360
        
        # 16 compass points
        directions = [
            "N", "NNE", "NE", "ENE", 
            "E", "ESE", "SE", "SSE", 
            "S", "SSW", "SW", "WSW", 
            "W", "WNW", "NW", "NNW"
        ]
        
        # Calculate index by dividing by 22.5 and rounding to nearest whole number
        index = int((degrees + 11.25) / 22.5) % 16
        
        return directions[index]

    def weatherCodeToText(self, code):
        """  Convert the  numeric weather code to text.
        """
        match code:
            case 0:
                return "Clear sky"
            case 1 | 2 | 3:
                return "Mainly clear, partly cloudy, and overcast"
            case 45 | 48:
                return "Fog and depositing rime fog"
            case 51 | 53 | 55:
                return "Drizzle: Light, moderate, and dense intensity"
            case 56 | 57:
                return "Freezing Drizzle: Light and dense intensity"
            case 61 | 63| 65:
                return "Rain: Slight, moderate and heavy intensity"
            case 66 | 67:
                return "Freezing Rain: Light and heavy intensity"
            case 71 | 73 | 75:
                return "Snow fall: Slight, moderate, and heavy intensity"
            case 77:
                return "Snow grains"
            case 80 | 81 | 82:
                return "Rain showers: Slight, moderate, and violent"
            case 85 | 86:
                return "Snow showers slight and heavy"
            case 95:
                return "Thunderstorm: Slight or moderate"
            case 96 | 99:
                return "Thunderstorm with slight and heavy hail"
            case _:
                return f"Invalid weather code {code}"

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