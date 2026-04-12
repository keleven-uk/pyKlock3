###############################################################################################################
#    stepWatchViewer.py    Copyright (C) <2026>  <Kevin Scott>                                                #
#                                                                                                             #
#    A class that displays the time within a matrix of words.                                                 #
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

import src.classes.stopWatch as sw

from PyQt6.QtWidgets import (QHBoxLayout, QVBoxLayout, QPushButton, QApplication, QFrame, QMainWindow, 
                             QGroupBox, QLCDNumber)
from PyQt6.QtCore    import QTimer


class StopWatch(QMainWindow):
    """  A class that displays as digital stop watch.
    """
    def __init__(self, parent):
        super().__init__()

        self.stopWatch = sw.timer()
        self.parent    = parent

        height     = 400
        width      = 900
        screenSize = QApplication.primaryScreen().availableGeometry()
        xPos       = int((screenSize.width() / 2)  - (width / 2))
        yPos       = int((screenSize.height() / 2) - (height / 2))

        self.parent.hide()

        self.setGeometry(xPos, yPos, width, height)
        self.setWindowTitle("pyStopWatch")

        self.buildGUI()
        
    def buildGUI(self):
        """  Build the GUI elements.
        """
        centralWidget = QFrame()
        self.setCentralWidget(centralWidget)
        centralLayout = QVBoxLayout()
        ButtonLayout  = QHBoxLayout()
        timerLayout   = QVBoxLayout()

        swGroup  = QGroupBox("Stop Watch")

        #  Create an lcd Number display.
        self.lcdTime = QLCDNumber()
        self.lcdTime.setDigitCount(11)                                # Display 8 digits
        self.lcdTime.display("00:00:00.00")                           # Show some initial value
        self.lcdTime.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)  # Use filled segment style

        self.btnStart = QPushButton(text="Start", parent=self)
        self.btnStart.clicked.connect(self.startTimer)
        self.btnStart.setEnabled(True)
        self.btnPause = QPushButton(text="Pause", parent=self)
        self.btnPause.clicked.connect(self.pauseTimer)
        self.btnPause.setEnabled(False)
        self.btnResume = QPushButton(text="Resume", parent=self)
        self.btnResume.clicked.connect(self.resumeTimer)
        self.btnResume.setEnabled(False)
        self.btnStop = QPushButton(text="Stop", parent=self)
        self.btnStop.clicked.connect(self.stopTimer)
        self.btnStop.setEnabled(False)
        self.btnClear = QPushButton(text="Clear", parent=self)
        self.btnClear.clicked.connect(self.clearTimer)
        self.btnClear.setEnabled(False)
        self.btnClose = QPushButton(text="Close", parent=self)
        self.btnClose.clicked.connect(self.close)

        ButtonLayout.addWidget(self.btnStart)
        ButtonLayout.addWidget(self.btnPause)
        ButtonLayout.addWidget(self.btnResume)
        ButtonLayout.addWidget(self.btnStop)
        ButtonLayout.addWidget(self.btnClear)
        ButtonLayout.addWidget(self.btnClose)

        timerLayout.addWidget(self.lcdTime)
        timerLayout.addLayout(ButtonLayout)

        swGroup.setLayout(timerLayout)

        centralLayout.addWidget(swGroup)
        centralWidget.setLayout(centralLayout)

        #  Set up short timer to update the clock every second
        self.Timer = QTimer(self)
        self.Timer.timeout.connect(self.updateTime)
        self.Timer.start(10)

    # ----------------------------------------------------------------------------------------------------------------------- updateTime() ----------
    def updateTime(self):
        self.lcdTime.display(self.stopWatch.elapsedTime)
    # ----------------------------------------------------------------------------------------------------------------------- startTimer() ----------
    def startTimer(self, event):
        self.stopWatch.start()
        self.btnStart.setEnabled(False)
        self.btnPause.setEnabled(True)
        self.btnStop.setEnabled(True)
    # ----------------------------------------------------------------------------------------------------------------------- pauseTimer() ----------
    def pauseTimer(self, event):
        self.stopWatch.pause()
        self.btnPause.setEnabled(False)
        self.btnResume.setEnabled(True)
        self.btnClear.setEnabled(True)
    # ----------------------------------------------------------------------------------------------------------------------- resumeTimer() ---------
    def resumeTimer(self, event):
        self.stopWatch.resume()
        self.btnPause.setEnabled(True)
        self.btnResume.setEnabled(False)
    # ----------------------------------------------------------------------------------------------------------------------- stopTimer() -----------
    def stopTimer(self, event):
        self.stopWatch.stop()
        self.btnStart.setEnabled(True)
        self.btnPause.setEnabled(False)
        self.btnResume.setEnabled(False)
        self.btnClear.setEnabled(True)
        self.btnStop.setEnabled(False)
    # ----------------------------------------------------------------------------------------------------------------------- clearTimer() ----------
    def clearTimer(self, event):
        self.stopWatch.clear()
        self.btnPause.setEnabled(False)
        self.btnStop.setEnabled(False)
        self.btnStart.setEnabled(True)
        self.btnStop.setEnabled(False)
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        self.Timer.stop()
        self.parent.show()
        event.accept()

 

