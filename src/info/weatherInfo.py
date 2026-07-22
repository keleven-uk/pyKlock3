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

import src.utils.weatherUtils as wu

from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QFrame, QWidget, QTabWidget, 
                            QGroupBox, QGridLayout, QLabel,)
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
    """
    current = self.weatherData.getCurrentWeather()

    page   = QWidget(self.twTab)
    layout = QFormLayout()
    layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
    page.setLayout(layout)

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