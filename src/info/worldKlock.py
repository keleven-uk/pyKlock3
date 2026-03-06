###############################################################################################################
#   worldKlock.py   Copyright (C) <2026>  <Kevin Scott>                                                       #
#                                                                                                             #
#    The methods for displaying a world Klock.                                                                #
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

import zoneinfo as zi

from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
                            QGroupBox, QGridLayout, QLabel, QComboBox)
from PyQt6.QtCore    import Qt, QTimer

import src.utils.klock_utils as utils

def buildGUI(self):
    """  Build the GUI elements.
    """
    #  Create a central widget.
    self.centralWidget = QFrame()
    self.setCentralWidget(self.centralWidget)
    self.centralLayout = QVBoxLayout()
    self.ButtonLayout  = QHBoxLayout()

    self.wkGroup  = QGroupBox("World Klock")
    self.wkLayout = QGridLayout(self.wkGroup)

    self.txtLegend    = QLabel("Shows the local time for the selected time zone.")
    self.txtLocalTime = QLabel("Local Time")
    self.txtLocalTime.setStyleSheet("font-size: 24pt;")
    self.lblLocalTime = QLabel("12:34:56")
    self.lblLocalTime.setStyleSheet("font-size: 24pt;")
    self.txtWorldTime = QLabel("World Klock Time")
    self.txtWorldTime.setStyleSheet("font-size: 24pt;")
    self.lblWorldTime = QLabel("12:34:56")
    self.lblWorldTime.setStyleSheet("font-size: 24pt;")
    self.txtTimeZone  = QLabel("Time Zone")
    self.txtTimeZone.setStyleSheet("font-size: 24pt;")
    self.cbTimeZone   = QComboBox()

    self.cbTimeZone.insertItems(0, utils.getTimezones())
    self.cbTimeZone.setCurrentText("GMT")

    #  callback needed to pass self as argument to update()
    cbTypeOfEasterCallback = functools.partial(update, self)
    self.cbTimeZone.currentTextChanged.connect(cbTypeOfEasterCallback)

    self.wkLayout.addWidget(self.txtLegend,    0, 0, Qt.AlignmentFlag.AlignLeft)
    self.wkLayout.addWidget(self.txtLocalTime, 1, 0, Qt.AlignmentFlag.AlignLeft)
    self.wkLayout.addWidget(self.lblLocalTime, 1, 1, Qt.AlignmentFlag.AlignCenter)
    self.wkLayout.addWidget(self.txtWorldTime, 2, 0, Qt.AlignmentFlag.AlignLeft)
    self.wkLayout.addWidget(self.lblWorldTime, 2, 1, Qt.AlignmentFlag.AlignCenter)
    self.wkLayout.addWidget(self.txtTimeZone,  4, 0, Qt.AlignmentFlag.AlignCenter)
    self.wkLayout.addWidget(self.cbTimeZone,   4, 1, Qt.AlignmentFlag.AlignLeft)

    self.wkGroup.setLayout(self.wkLayout)

    btnClose = QPushButton(text="Close", parent=self)
    btnClose.clicked.connect(self.close)

    self.ButtonLayout.addWidget(btnClose)

    self.centralLayout.addWidget(self.wkGroup)
    self.centralLayout.addLayout(self.ButtonLayout)

    self.centralWidget.setLayout(self.centralLayout)

    #  Set up short timer to update the clock every second
    #  callback needed to pass self as argument to update()
    timerCallback = functools.partial(update, self)
    self.Timer = QTimer(self)
    self.Timer.timeout.connect(timerCallback)
    self.Timer.start(1000)

# ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
def update(self):
    """    Updated the labels.
    """
    localNow = datetime.datetime.now()
    worldNow = datetime.datetime.now(zi.ZoneInfo(self.cbTimeZone.currentText()))

    self.lblLocalTime.setText(localNow.strftime("%H %M %S"))
    self.lblWorldTime.setText(worldNow.strftime("%H %M %S"))
# ----------------------------------------------------------------------------------------------------------------------- close() -------------------
def close(self):
    """  Close down the time when not needed.
    """
    if self.Timer:
        self.Timer.stop()