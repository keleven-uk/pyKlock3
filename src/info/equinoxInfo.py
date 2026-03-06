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

import functools
import datetime

from pymeeus.Sun import Sun

from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
                            QGroupBox, QGridLayout, QLabel, QSpinBox)
from PyQt6.QtCore    import Qt

def buildGUI(self):
    """  Build the GUI elements.
    """
    #  Create a central widget.
    self.centralWidget = QFrame()
    self.setCentralWidget(self.centralWidget)
    self.centralLayout = QVBoxLayout()
    self.ButtonLayout  = QHBoxLayout()

    self.seGroup  = QGroupBox("Seasons Equinox")
    self.seLayout = QGridLayout(self.seGroup)

    self.txtLegend        = QLabel("Shows the date of the seasonal equinox.")
    self.txtSpring        = QLabel("Spring Equinox")
    self.lblSpring        = QLabel("03 April 2026")
    self.txtSummer        = QLabel("Summer Equinox")
    self.lblSummer        = QLabel("05 April 2026")
    self.txtAutumn        = QLabel("Autumn Equinox")
    self.lblAutumn        = QLabel("06 April 2026")
    self.txtWinter        = QLabel("Winter Equinox")
    self.lblWinter        = QLabel("06 April 2026")
    self.txtYearOfEquinox = QLabel("Year")
    self.sbYearOfEquinox  = QSpinBox(self)

    currentYear = datetime.datetime.now().year

    self.sbYearOfEquinox.setMinimum(1)
    self.sbYearOfEquinox.setMaximum(3000)
    self.sbYearOfEquinox.setValue(currentYear)

    #  callback needed to pass self as argument to update()
    sbYearOfEquinoxCallback = functools.partial(update, self)
    self.sbYearOfEquinox.valueChanged.connect(sbYearOfEquinoxCallback)

    self.seLayout.addWidget(self.txtLegend,        0, 0, Qt.AlignmentFlag.AlignLeft)
    self.seLayout.addWidget(self.txtSpring,        1, 0, Qt.AlignmentFlag.AlignCenter)
    self.seLayout.addWidget(self.lblSpring,        1, 1, Qt.AlignmentFlag.AlignLeft)
    self.seLayout.addWidget(self.txtSummer,        2, 0, Qt.AlignmentFlag.AlignCenter)
    self.seLayout.addWidget(self.lblSummer,        2, 1, Qt.AlignmentFlag.AlignLeft)
    self.seLayout.addWidget(self.txtAutumn,        3, 0, Qt.AlignmentFlag.AlignCenter)
    self.seLayout.addWidget(self.lblAutumn,        3, 1, Qt.AlignmentFlag.AlignLeft)
    self.seLayout.addWidget(self.txtWinter,        4, 0, Qt.AlignmentFlag.AlignCenter)
    self.seLayout.addWidget(self.lblWinter,        4, 1, Qt.AlignmentFlag.AlignLeft)
    self.seLayout.addWidget(self.txtYearOfEquinox, 5, 0, Qt.AlignmentFlag.AlignCenter)
    self.seLayout.addWidget(self.sbYearOfEquinox,  5, 1, Qt.AlignmentFlag.AlignLeft)

    self.seGroup.setLayout(self.seLayout)

    btnClose = QPushButton(text="Close", parent=self)
    btnClose.clicked.connect(self.close)

    self.ButtonLayout.addWidget(btnClose)

    self.centralLayout.addWidget(self.seGroup)
    self.centralLayout.addLayout(self.ButtonLayout)

    self.centralWidget.setLayout(self.centralLayout)

# ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
def update(self):
    """    Updated the labels.
    """
    epoch = Sun.get_equinox_solstice(self.sbYearOfEquinox.value(), target="spring")
    y, m, d, h, mi, s = epoch.get_full_date()
    self.lblSpring.setText(f" {d}/{m}/{y}  {h:02}:{mi:02}")

    epoch = Sun.get_equinox_solstice(self.sbYearOfEquinox.value(), target="summer")
    y, m, d, h, mi, s = epoch.get_full_date()
    self.lblSummer.setText(f" {d}/{m}/{y}  {h:02}:{mi:02}")

    epoch = Sun.get_equinox_solstice(self.sbYearOfEquinox.value(), target="autumn")
    y, m, d, h, mi, s = epoch.get_full_date()
    self.lblAutumn.setText(f" {d}/{m}/{y}  {h:02}:{mi:02}")

    epoch = Sun.get_equinox_solstice(self.sbYearOfEquinox.value(), target="winter")
    y, m, d, h, mi, s = epoch.get_full_date()
    self.lblWinter.setText(f" {d}/{m}/{y}  {h:02}:{mi:02}")