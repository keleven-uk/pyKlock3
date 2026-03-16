###############################################################################################################
#    publicHolidays.py   Copyright (C) <2026>  <Kevin Scott>                                                  #
#                                                                                                             #
#    The methods for displaying Public Holidays dates for a given year and country.                           #
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

import functools
import datetime

import workalendar.registry

from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy,
                            QGroupBox, QGridLayout, QLabel, QComboBox, QSpinBox, QListWidget)
from PyQt6.QtCore    import Qt

def init(self):
    """  Execute some initialising stuff.
    """
    self.countryNames = []
    self.countryCodes = []

    calendars = workalendar.registry.registry.get_calendars()  # This returns a dictionary
    for code, calendar_class in calendars.items():
        self.countryCodes.append(code.replace("'", ""))
        self.countryNames.append(f"{calendar_class.name!r}".replace("'", ""))

    self.displayNames = sorted(self.countryNames)
    
    self.UK = self.displayNames.index("United Kingdom")

def buildGUI(self):
    """  Build the GUI elements.
    """
    #  Create a central widget.
    self.centralWidget = QFrame()
    self.setCentralWidget(self.centralWidget)
    self.centralLayout = QVBoxLayout()
    self.ButtonLayout  = QHBoxLayout()

    self.phGroup  = QGroupBox("Public Holidays")
    self.phLayout = QGridLayout(self.phGroup)

    self.txtLegend  = QLabel("Displaying Public Holidays dates for a given year and country. ")
    self.lwHolidays = QListWidget(self)
    self.lwDates    = QListWidget(self)
    self.spacer     = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    self.txtCountry = QLabel("Country")
    self.cbCountry  = QComboBox()
    self.txtYear    = QLabel("Year")
    self.sbYear     = QSpinBox(self)

    self.cbCountry.insertItems(self.UK, self.displayNames)
    self.cbCountry.setCurrentIndex(self.UK)

    #  callback needed to pass self as argument to update()
    cbCountryCallback = functools.partial(update, self)
    self.cbCountry.currentTextChanged.connect(cbCountryCallback)

    currentYear = datetime.datetime.now().year

    self.sbYear.setMinimum(1)
    self.sbYear.setMaximum(3000)
    self.sbYear.setValue(currentYear)

    #  callback needed to pass self as argument to update()
    sbYearCallback = functools.partial(update, self)
    self.sbYear.valueChanged.connect(sbYearCallback)

    self.phLayout.addWidget(self.txtLegend,    1, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)
    self.phLayout.addWidget(self.lwHolidays,   2, 0, Qt.AlignmentFlag.AlignLeft)
    self.phLayout.addWidget(self.lwDates,      2, 1, Qt.AlignmentFlag.AlignLeft)
    self.phLayout.addItem(self.spacer)                                                  #  Removed the extra space after the list boxes.
    self.phLayout.addWidget(self.txtCountry,   4, 0, Qt.AlignmentFlag.AlignCenter)
    self.phLayout.addWidget(self.cbCountry,    4, 1, Qt.AlignmentFlag.AlignLeft)
    self.phLayout.addWidget(self.txtYear,      6, 0, Qt.AlignmentFlag.AlignCenter)
    self.phLayout.addWidget(self.sbYear,       6, 1, Qt.AlignmentFlag.AlignLeft)

    self.phGroup.setLayout(self.phLayout)

    btnClose = QPushButton(text="Close", parent=self)
    btnClose.clicked.connect(self.close)

    self.ButtonLayout.addWidget(btnClose)

    self.centralLayout.addWidget(self.phGroup)
    self.centralLayout.addLayout(self.ButtonLayout)

    self.centralWidget.setLayout(self.centralLayout)

# ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
def update(self):
    """    Updated the list box widgets.
    """
    self.lwHolidays.clear()
    self.lwDates.clear()

    year     = self.sbYear.value()
    country  = self.cbCountry.currentText()
    index    = self.countryNames.index(self.cbCountry.currentText())

    self.txtLegend.setText(f"Displaying Public Holidays dates for {country} in {year}. ")

    CalendarClass = workalendar.registry.registry.get(self.countryCodes[index])
    calendar      = CalendarClass()
    hols          = calendar.holidays(year)

    for hol in hols:
        self.lwHolidays.addItem(hol[1].replace("'", ""))
        self.lwDates.addItem(hol[0].strftime("%d %B %Y"))
