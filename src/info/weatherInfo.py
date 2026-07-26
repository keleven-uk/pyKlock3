###############################################################################################################
#   equinoxInfo.py   Copyright (C) <2026>  <Kevin Scott>                                                      #
#                                                                                                             #
#    The methods for displaying equinox dates for a given year.                                               #
#                                                                                                             #
#    For changes see history.txt                                                                              #
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
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, timezone

import src.utils.weatherUtils as wu

from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QFrame, QWidget, QTabWidget, 
                            QLabel,)
from PyQt6.QtCore    import Qt

def initWeather(self, myConfig, myLogger):
    self.weatherData = wu.Weather(myConfig, myLogger)
    self.weatherData.connect()
    
def buildGUI(self):
    """  Build the GUI elements.
    """
    #  Create a central widget.
    self.centralWidget = QFrame()
    self.setCentralWidget(self.centralWidget)
    self.centralLayout = QVBoxLayout()
    self.ButtonLayout  = QHBoxLayout()

    btnClose = QPushButton(text="Close", parent=self)
    btnClose.clicked.connect(self.close)

    self.ButtonLayout.addWidget(btnClose)

    self.twTab = QTabWidget()

    funcs = [Current, Forecast]

    for func in funcs:          #  Add the individual tabs.  For a tab to be added - insert title into the list funcs.
        func(self)

    self.centralLayout.addWidget(self.twTab)
    self.centralLayout.addLayout(self.ButtonLayout)

    self.centralWidget.setLayout(self.centralLayout)

# ----------------------------------------------------------------------------------------------------------------------- Info() ----------------
def Current(self):
    """  Display Current Weather.

         "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "wind_direction_10m", 
                        "wind_speed_10m", "wind_gusts_10m", "precipitation", "showers", "rain", "weather_code", "cloud_cover", 
                        "pressure_msl", "surface_pressure"],

        Order is important.
    """
    response = self.weatherData.getCurrentWeather()
    current  = response.Current()

    page   = QWidget(self.twTab)
    layout = QFormLayout()
    layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
    page.setLayout(layout)

    utcOffsetSec = response.UtcOffsetSeconds()
    local_tz     = timezone(timedelta(seconds=utcOffsetSec))

    layout.addRow("Current Weather",  QLabel(f"Updated every 15 minutes"))
    layout.addRow("----------------------------",  QLabel(f"------------------------------------------------"))
    layout.addRow("Coordinates",                   QLabel(f"{response.Latitude()}°N : {response.Longitude()}°E"))
    layout.addRow("Elevation",                     QLabel(f"{response.Elevation()} m asl"))
    layout.addRow("Current Time",                  QLabel(f"{datetime.fromtimestamp(current.Time(), tz=local_tz)}"))
    layout.addRow("Timezone difference to GMT+0",  QLabel(f"{response.UtcOffsetSeconds()} secs"))
    layout.addRow("Current Weather",               QLabel(f"{self.weatherData.weatherCodeToText(current.Variables(10).Value())}"))

    if current.Variables(3).Value():
        layout.addRow("Day / Night", QLabel(f"Day"))
    else:
        layout.addRow("Day / Night", QLabel(f"Night"))
    layout.addRow("----------------------------",  QLabel(f"------------------------------------------------"))

    layout.addRow("Current Temperature",           QLabel(f"{current.Variables(0).Value():.2f} °C"))
    layout.addRow("Current Apparent Temperature ", QLabel(f"{current.Variables(2).Value():.2f} °C"))
    layout.addRow("Current Relative Humidity",     QLabel(f"{current.Variables(1).Value():.2f}"))
    layout.addRow("Current Wind Direction",        QLabel(f"{self.weatherData.degreesToText(current.Variables(4).Value())}"))
    layout.addRow("Current Wind Speed",            QLabel(f"{current.Variables(5).Value():.2f} km/h"))
    layout.addRow("Current Wind Gust",             QLabel(f"{current.Variables(6).Value():.2f} km/h"))
    layout.addRow("Current Precipitation",         QLabel(f"{current.Variables(7).Value():.2f} mm"))
    layout.addRow("Current Showers",               QLabel(f"{current.Variables(8).Value():.2f} mm"))
    layout.addRow("Current Rain",                  QLabel(f"{current.Variables(9).Value():.2f} mm"))
    layout.addRow("Current Cloud Cover",           QLabel(f"{current.Variables(11).Value():.2f} %"))
    layout.addRow("Current Pressure",              QLabel(f"{current.Variables(12).Value():.2f} hpa"))
    layout.addRow("Current Surface Pressure",      QLabel(f"{current.Variables(13).Value():.2f} hpa"))
    
    self.twTab.addTab(page, "Current Weather")
# ----------------------------------------------------------------------------------------------------------------------- Info() ----------------
def Forecast(self):
    """  Display Weather Forecast.
    """
    page   = QWidget(self.twTab)
    layout = QFormLayout()
    layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
    page.setLayout(layout)

    self.twTab.addTab(page, "Weather Forecast")
# ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
def update(self):
    """    Updated the labels.
    """
    pass