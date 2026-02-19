###############################################################################################################
#    NTPViewer   Copyright (C) <2026>  <Kevin Scott>                                                          #
#                                                                                                             #
#    Display NTP Server time.                                                                                 #
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

import ntplib

from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow, QFrame, QApplication,
                            QGroupBox, QGridLayout, QLabel)
from PyQt6.QtCore    import Qt, QTimer

import src.classes.friendsStore as fs
import src.classes.styles as styles

import src.windows.friendsAdd as af

class NTPViewer(QMainWindow):
    """  Display results from a NTP server in a separate window.
    """
    def __init__(self, myLogger, myConfig):
        super().__init__()

        self.logger = myLogger
        self.config = myConfig
        self.styles = styles.Styles()
        self.client = ntplib.NTPClient()

        self.height      = 400
        self.width       = 400
        self.screenSize  = QApplication.primaryScreen().availableGeometry()
        self.xPos        = int((self.screenSize.width() / 2)  - (self.width / 2))
        self.yPos        = int((self.screenSize.height() / 2) - (self.height / 2))

        self.setGeometry(self.xPos, self.yPos, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("Friends")

        self.buildGUI()
        self.updateTime()

    def buildGUI(self):
        """  Build the GUI elements.
        """
        #  Create a central widget.
        self.centralWidget = QFrame()
        self.centralWidget.setStyleSheet("margin:0px; border:0px")
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

        self.ntpGroup.setStyleSheet(self.styles.QGroupBox_STYLE)
        self.ntpGroup.setLayout(self.ntpLayout)

        btnClose = QPushButton(text="Close", parent=self)
        btnClose.clicked.connect(self.close)

        self.ButtonLayout.addWidget(btnClose)

        self.centralLayout.addWidget(self.ntpGroup)
        self.centralLayout.addLayout(self.ButtonLayout)

        self.centralWidget.setLayout(self.centralLayout)

        #  Set up short timer to update the clock every second
        self.Timer = QTimer(self)
        self.Timer.timeout.connect(self.updateTime)
        self.Timer.start(1000)
 
     # ----------------------------------------------------------------------------------------------------------------------- updateTime() ----------
    def updateTime(self):
        """  Update the time every second.
        """
        try:
            response = self.client.request('time.enhost.uk')
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
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        """  When the viewer is closed, checks if any child windows are still open.
        """
        event.accept()


