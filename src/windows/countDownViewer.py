###############################################################################################################
#    countDownViewer.py    Copyright (C) <2026>  <Kevin Scott>                                                #
#                                                                                                             #
#    A class that displays A count down timer.                                                                #
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

import src.classes.countDown as cd

from PyQt6.QtWidgets import (QHBoxLayout, QVBoxLayout, QPushButton, QApplication, QFrame, QMainWindow, 
                             QGroupBox, QLCDNumber)
from PyQt6.QtCore    import QTimer


class CountDown(QMainWindow):
    """  A class that displays as digital count down timer.
    """
    def __init__(self, parent):
        super().__init__()

        self.countDown = cd.countdown(self)
        self.parent    = parent

        height     = 400
        width      = 900
        screenSize = QApplication.primaryScreen().availableGeometry()
        xPos       = int((screenSize.width() / 2)  - (width / 2))
        yPos       = int((screenSize.height() / 2) - (height / 2))

        self.parent.hide()

        self.setGeometry(xPos, yPos, width, height)
        self.setWindowTitle("Count Down Timer")

        self.buildGUI()
        
    def buildGUI(self):
        """  Build the GUI elements.
        """
        centralWidget = QFrame()
        self.setCentralWidget(centralWidget)
        centralLayout = QVBoxLayout()
        ButtonLayout  = QHBoxLayout()
        timerLayout   = QVBoxLayout()

        swGroup  = QGroupBox("Count Down Timer")

        #  Create an lcd Number display.
        self.lcdTime = QLCDNumber()
        self.lcdTime.setDigitCount(8)                                 # Display 8 digits
        self.lcdTime.display("00:00:00")                              # Show some initial value
        self.lcdTime.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)  # Use filled segment style

        self.btn15min = QPushButton(text="15", parent=self)
        self.btn15min.setObjectName("15")
        self.btn15min.clicked.connect(self.startTimer)
        self.btn15min.setEnabled(True)
        self.btn30min = QPushButton(text="30", parent=self)
        self.btn30min.setObjectName("30")
        self.btn30min.clicked.connect(self.startTimer)
        self.btn30min.setEnabled(True)
        self.btn45min = QPushButton(text="45", parent=self)
        self.btn45min.setObjectName("45")
        self.btn45min.clicked.connect(self.startTimer)
        self.btn45min.setEnabled(True)
        self.btn60min = QPushButton(text="60", parent=self)
        self.btn60min.setObjectName("60")
        self.btn60min.clicked.connect(self.startTimer)
        self.btn60min.setEnabled(True)
        self.btnStop = QPushButton(text="Stop", parent=self)
        self.btnStop.clicked.connect(self.stopTimer)
        self.btnStop.setEnabled(False)
        self.btnClose = QPushButton(text="Close", parent=self)
        self.btnClose.clicked.connect(self.close)
        self.btnClose.setEnabled(True)

        ButtonLayout.addWidget(self.btn15min)
        ButtonLayout.addWidget(self.btn30min)
        ButtonLayout.addWidget(self.btn45min)
        ButtonLayout.addWidget(self.btn60min)
        ButtonLayout.addWidget(self.btnStop)
        ButtonLayout.addWidget(self.btnClose)

        timerLayout.addWidget(self.lcdTime)
        timerLayout.addLayout(ButtonLayout)

        swGroup.setLayout(timerLayout)

        centralLayout.addWidget(swGroup)
        centralWidget.setLayout(centralLayout)

        #  Set up short timer to update the clock every second
        self.Timer = QTimer(self)
        self.Timer.timeout.connect(self.updateTime)
        self.Timer.start(1000)

    # ----------------------------------------------------------------------------------------------------------------------- updateTime() ----------
    def updateTime(self):
        if self.countDown.countdownRunning:
            self.lcdTime.display(self.countDown.elapsedTime)
    # ----------------------------------------------------------------------------------------------------------------------- startTimer() ----------
    def startTimer(self, event):
        action    = self.sender()
        name      = action.objectName()

        match name:
            case "15":
                target = 15
            case "30":
                target = 30
            case "45":
                target = 45
            case "60":
                target = 60

        self.countDown.start(target)
        self.btn15min.setEnabled(False)
        self.btn30min.setEnabled(False)
        self.btn45min.setEnabled(False)
        self.btn60min.setEnabled(False)
        self.btnStop.setEnabled(True)
    # ----------------------------------------------------------------------------------------------------------------------- stopTimer() -----------
    def stopTimer(self, event):
        self.countDown.clear()
        self.lcdTime.display("00:00:00")
        self.btn15min.setEnabled(True)
        self.btn30min.setEnabled(True)
        self.btn45min.setEnabled(True)
        self.btn60min.setEnabled(True)
        self.btnStop.setEnabled(False)
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        self.Timer.stop()
        self.parent.show()
        event.accept()

 

