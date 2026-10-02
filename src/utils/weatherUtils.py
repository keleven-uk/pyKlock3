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

# pip install openmeteo-requests

import openmeteo_requests

import requests
import pandas as pd

class Weather():

    def __init__(self, myConfig, myLogger):
        self.config = myConfig
        self.logger = myLogger
    # ----------------------------------------------------------------------------------------------------------------------- connect() -------------
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
    # ----------------------------------------------------------------------------------------------------------------------- getCurrentWeathert() --
    def getCurrentWeather(self):
        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": self.config.LATITUDE,
            "longitude": self.config.LONGITUDE,
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
    # ----------------------------------------------------------------------------------------------------------------------- get7DayForcast() ------
    def get7DayForcast(self):
        """
        """
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": self.config.LATITUDE,
            "longitude": self.config.LONGITUDE,
            "hourly": ["temperature_2m", "precipitation_probability", "wind_speed_10m", "wind_direction_10m", "weather_code"],
        }
                #  Execute the API Request with network exception handling
        try:
            responses = self.openmeteo.weather_api(url, params = params)
            
            if not responses:
                self.logger.error("Error: Received an empty response array from the API.")
                return None
                
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

        response = responses[0]
        print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation: {response.Elevation()} m asl")
        print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
        hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()
        hourly_wind_direction_10m = hourly.Variables(3).ValuesAsNumpy()
        hourly_weather_code = hourly.Variables(4).ValuesAsNumpy()

        hourly_data = {
            "date": pd.date_range(
                start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
                end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
                freq = pd.Timedelta(seconds = hourly.Interval()),
                inclusive = "left"
            )
        }

        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["precipitation_probability"] = hourly_precipitation_probability
        hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
        hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
        hourly_data["weather_code"] = hourly_weather_code

        hourly_dataframe = pd.DataFrame(data = hourly_data)
        print("\nHourly data\n", hourly_dataframe)

        print(hourly_dataframe.head())


        # params = {
        #     "latitude": self.config.LATITUDE,
        #     "longitude": self.config.LONGITUDE,
        #     "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_probability_max"],
        #     "timezone": "auto"
        # }

        # url = "https://api.open-meteo.com/v1/forecast"
        # response = requests.get(url, params=params).json()

        # # Parse the 7-day daily data structure
        # daily_data = response["daily"]
        # df = pd.DataFrame(daily_data)
        # print(df)

    # ----------------------------------------------------------------------------------------------------------------------- degreesToText() -------
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
    # ----------------------------------------------------------------------------------------------------------------------- weatherCodeToText(() --
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