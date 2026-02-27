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

from pymeeus.Epoch import Epoch
from pymeeus.Sun import Sun

from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
                            QGroupBox, QGridLayout, QLabel, QComboBox, QSpinBox)
from PyQt6.QtCore    import Qt

def buildGUI(self):
    """  Build the GUI elements.
    """
    #  Create a central widget.
    self.centralWidget = QFrame()
    self.setCentralWidget(self.centralWidget)
    self.centralLayout = QVBoxLayout()
    self.ButtonLayout  = QHBoxLayout()

    self.ntpGroup  = QGroupBox("Easter Dates")
    self.ntpLayout = QGridLayout(self.ntpGroup)

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

    self.ntpLayout.addWidget(self.txtSpring,        0, 0, Qt.AlignmentFlag.AlignCenter)
    self.ntpLayout.addWidget(self.lblSpring,        0, 1, Qt.AlignmentFlag.AlignLeft)
    self.ntpLayout.addWidget(self.txtSummer,        1, 0, Qt.AlignmentFlag.AlignCenter)
    self.ntpLayout.addWidget(self.lblSummer,        1, 1, Qt.AlignmentFlag.AlignLeft)
    self.ntpLayout.addWidget(self.txtAutumn,        2, 0, Qt.AlignmentFlag.AlignCenter)
    self.ntpLayout.addWidget(self.lblAutumn,        2, 1, Qt.AlignmentFlag.AlignLeft)
    self.ntpLayout.addWidget(self.txtWinter,        3, 0, Qt.AlignmentFlag.AlignCenter)
    self.ntpLayout.addWidget(self.lblWinter,        3, 1, Qt.AlignmentFlag.AlignLeft)
    self.ntpLayout.addWidget(self.txtYearOfEquinox, 5, 0, Qt.AlignmentFlag.AlignCenter)
    self.ntpLayout.addWidget(self.sbYearOfEquinox,  5, 1, Qt.AlignmentFlag.AlignLeft)

    self.ntpGroup.setLayout(self.ntpLayout)

    btnClose = QPushButton(text="Close", parent=self)
    btnClose.clicked.connect(self.close)

    self.ButtonLayout.addWidget(btnClose)

    self.centralLayout.addWidget(self.ntpGroup)
    self.centralLayout.addLayout(self.ButtonLayout)

    self.centralWidget.setLayout(self.centralLayout)

# ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
def update(self):
    """    Updated the labels.
    """
    epoch = Sun.get_equinox_solstice(self.sbYearOfEquinox.value(), target="spring")
    y, m, d, h, mi, s = epoch.get_full_date()
    self.lblSpring.setText(f" {d}/{m}/{y}  {h}:{mi}")

    epoch = Sun.get_equinox_solstice(self.sbYearOfEquinox.value(), target="summer")
    y, m, d, h, mi, s = epoch.get_full_date()
    self.lblSummer.setText(f" {d}/{m}/{y}  {h}:{mi}")

    epoch = Sun.get_equinox_solstice(self.sbYearOfEquinox.value(), target="autumn")
    y, m, d, h, mi, s = epoch.get_full_date()
    self.lblAutumn.setText(f" {d}/{m}/{y}  {h}:{mi}")

    epoch = Sun.get_equinox_solstice(self.sbYearOfEquinox.value(), target="winter")
    y, m, d, h, mi, s = epoch.get_full_date()
    self.lblWinter.setText(f" {d}/{m}/{y}  {h}:{mi}")