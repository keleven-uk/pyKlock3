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

from pyqttoast import Toast, ToastPreset

from PyQt6.QtWidgets import (QHBoxLayout, QVBoxLayout, QPushButton, QApplication, QFrame, QMainWindow, 
                             QGroupBox, QLCDNumber)


class CountDown(QMainWindow):
    """  A class that displays as digital count down timer.
    """
    def __init__(self, parent):
        super().__init__()

        self.countDown = cd.countdown(self)
        self.countDown.countDownTick.connect(self.updateTime)                 #  Signal is fired when the count down is running, update display.
        self.countDown.countDownEnd.connect(self.endEvent)                    #  Signal is fired when the count down has ended.

        self.parent = parent

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
        self.btnStop.clicked.connect(self.stop)
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

    # ----------------------------------------------------------------------------------------------------------------------- updateTime() ----------
    def updateTime(self):
        """  Update the LCD display with the current count down value.
        """
        self.lcdTime.display(self.countDown.elapsedTime)
    # ----------------------------------------------------------------------------------------------------------------------- startTimer() ----------
    def startTimer(self, event):
        """  When a time interval is selected, start the count down timer with that value.

             Switch off the unwanted buttons.
        """
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
        self.lcdTime.display(self.countDown.elapsedTime)
        self.btn15min.setEnabled(False)
        self.btn30min.setEnabled(False)
        self.btn45min.setEnabled(False)
        self.btn60min.setEnabled(False)
        self.btnStop.setEnabled(True)
    # ----------------------------------------------------------------------------------------------------------------------- stopTimer() -----------
    def stop(self, event):
        """  Called when the stop button is called.
        """
        self.resetButtons()
    # ----------------------------------------------------------------------------------------------------------------------- stopTimer() -----------
    def endEvent(self):
        """  Called when the count down ends - when toe time interval is fully elapsed.
        """
        self.resetButtons()

        toast = Toast(self.parent)
        toast.setDuration(0)        #  Do not timeout.
        toast.applyPreset(ToastPreset.INFORMATION_DARK)
        toast.setTitle("Count Down Timer")
        toast.setText("Count Down Timer Finished.")
        toast.show()
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        """  Called when the window is closed.
        """
        self.countDown.clear()
        self.parent.show()
        event.accept()

    def resetButtons(self):
        """  Resets the buttons to their initial state.
        """
        self.countDown.clear()
        self.lcdTime.display("00:00:00")

        self.btn15min.setEnabled(True)
        self.btn30min.setEnabled(True)
        self.btn45min.setEnabled(True)
        self.btn60min.setEnabled(True)
        self.btnStop.setEnabled(False)
