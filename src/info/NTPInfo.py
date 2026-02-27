###############################################################################################################
#    NTOInfo   Copyright (C) <2026>  <Kevin Scott>                                                            #
#                                                                                                             #
#    The methods for displaying NTP info.                                                                     #
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

import time
import functools

import ntplib

from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
                            QGroupBox, QGridLayout, QLabel)
from PyQt6.QtCore    import Qt, QTimer

# ----------------------------------------------------------------------------------------------------------------------- updateTime() --------------
def buildGUI(self):
    """  Build the GUI elements.
    """
    #  Create a central widget.
    self.centralWidget = QFrame()
    self.setCentralWidget(self.centralWidget)
    self.centralLayout = QVBoxLayout()
    self.ButtonLayout  = QHBoxLayout()

    self.ntpGroup   = QGroupBox("NTP Server Time")
    self.ntpLayout  = QGridLayout(self.ntpGroup)
    self.ntpText    = QLabel("NTP Server Time")
    self.ntpLabel   = QLabel("12:34:56:789")
    self.pcText     = QLabel("PC Time")
    self.pcLabel    = QLabel("12:34:56:789")
    self.difText    = QLabel("Difference Time")
    self.difLabel   = QLabel("0.00 Seconds")
    self.offText    = QLabel("NTP Offset")
    self.offLabel   = QLabel("0.00 Seconds")
    self.delayText  = QLabel("NTP Root Delay")
    self.delayLabel = QLabel("0.00 Seconds")

    self.ntpLayout.addWidget(self.ntpText,    0, 0, Qt.AlignmentFlag.AlignCenter)
    self.ntpLayout.addWidget(self.ntpLabel,   0, 1, Qt.AlignmentFlag.AlignLeft)
    self.ntpLayout.addWidget(self.pcText,     1, 0, Qt.AlignmentFlag.AlignCenter)
    self.ntpLayout.addWidget(self.pcLabel,    1, 1, Qt.AlignmentFlag.AlignLeft)
    self.ntpLayout.addWidget(self.difText,    2, 0, Qt.AlignmentFlag.AlignCenter)
    self.ntpLayout.addWidget(self.difLabel,   2, 1, Qt.AlignmentFlag.AlignLeft)
    self.ntpLayout.addWidget(self.offText,    3, 0, Qt.AlignmentFlag.AlignCenter)
    self.ntpLayout.addWidget(self.offLabel,   3, 1, Qt.AlignmentFlag.AlignLeft)
    self.ntpLayout.addWidget(self.delayText,  4, 0, Qt.AlignmentFlag.AlignCenter)
    self.ntpLayout.addWidget(self.delayLabel, 4, 1, Qt.AlignmentFlag.AlignLeft)

    self.ntpGroup.setLayout(self.ntpLayout)

    btnClose = QPushButton(text="Close", parent=self)
    btnClose.clicked.connect(self.close)

    self.ButtonLayout.addWidget(btnClose)

    self.centralLayout.addWidget(self.ntpGroup)
    self.centralLayout.addLayout(self.ButtonLayout)

    self.centralWidget.setLayout(self.centralLayout)

    self.client = ntplib.NTPClient()

    updateTime(self)

    #  Set up short timer to update the clock every second
    #  callback needed to pass self as argument to update()
    timerCallback = functools.partial(updateTime, self)
    self.Timer = QTimer(self)
    self.Timer.timeout.connect(timerCallback)
    self.Timer.start(1000)

# ----------------------------------------------------------------------------------------------------------------------- updateTime() --------------
def updateTime(self):
    """  Update the time every second.
    """
    try:
        response = self.client.request("time.enhost.uk")
        ntpTime  = response.tx_time
        offset   = response.offset
        delay    = response.root_delay

        pcTime = time.time()
        diff   = pcTime - ntpTime
        self.ntpLabel.setText(time.ctime(ntpTime))
        self.pcLabel.setText(time.ctime(pcTime))
        self.difLabel.setText(f" {diff:.2f} seconds")
        self.offLabel.setText(f" {offset:.2f} seconds")
        self.delayLabel.setText(f" {delay:.2f} seconds")
    except ntplib.NTPException:
        print("No response from server")
# ----------------------------------------------------------------------------------------------------------------------- close() -------------------
def close(self):
    """  Close down the time when not needed.
    """
    if self.Timer:
        self.Timer.stop()

