###############################################################################################################
#    textKlock.py    Copyright (C) <2026>  <Kevin Scott>                                                      #
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

from PyQt6.QtWidgets import (QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QApplication, QFrame, QMainWindow, 
                             QGroupBox, QLabel, QProgressBar)
from PyQt6.QtCore    import QTimer, QDateTime
from PyQt6.QtCore    import Qt

import src.classes.selectTime as st
import src.classes.styles as styles
import src.classes.systemInfo as si

import src.utils.textKlockCodes as tkc
import src.utils.klock_utils as utils


class textKlock(QMainWindow):
    """  A class that displays the time within a matrix of words.
    """
    def __init__(self, myConfig, parent):
        super().__init__()

        self.config     = myConfig
        self.selectTime = st.SelectTime()
        self.styles     = styles.Styles()             #  Styles for the battery progress bar.
        self.systemInfo = si.SysInfo()
        self.parent     = parent
        self.onColour   = self.config.TK_ON_COLOUR
        self.offColour  = self.config.TK_OFFOLOUR
        self.backColour = self.config.TK_BACKGROUND

        self.parent.hide()

        height     = 600
        width      = 400
        screenSize = QApplication.primaryScreen().availableGeometry()
        xPos       = int((screenSize.width() / 2)  - (width / 2))
        yPos       = int((screenSize.height() / 2) - (height / 2))

        self.setGeometry(xPos, yPos, height, width)
        self.setWindowTitle("pyKlock")

        self.buildGUI()
        self.buildStatusBar()

        self.updateTime
        self.allOn()


    def buildGUI(self):
        """  Build the GUI elements.
        """
        centralWidget = QFrame()
        self.setCentralWidget(centralWidget)
        centralLayout = QVBoxLayout()
        ButtonLayout  = QHBoxLayout()

        tkGroup  = QGroupBox("Text Klock")
        tkLayout = QGridLayout(tkGroup)
        
        self.addRow(tkLayout, ["I", "T", "E", "E", "I", "S", "K", "A", "T", "E", "N", "H", "A", "L", "F", "Q", "U", "A", "R", "T", "E", "R", "I", "X"], 0)
        self.addRow(tkLayout, ["T", "W", "E", "N", "T", "Y", "K", "F", "I", "V", "E", "J", "A", "B", "O", "U", "T", "P", "T", "O", "S", "F", "E", "W"], 1)
        self.addRow(tkLayout, ["P", "A", "S", "T", "K", "O", "N", "E", "L", "T", "W", "O", "O", "T", "H", "R", "E", "E", "C", "F", "O", "U", "R", "K"], 2)
        self.addRow(tkLayout, ["F", "I", "V", "E", "D", "S", "I", "X", "U", "S", "E", "V", "E", "N", "R", "E", "I", "G", "H", "T", "M", "T", "E", "N"], 3)
        self.addRow(tkLayout, ["N", "I", "N", "E", "K", "E", "L", "E", "V", "E", "N", "U", "T", "W", "E", "L", "V", "E", "T", "A", "S", "H", "O", "W"], 4)
        self.addRow(tkLayout, ["I", "N", "X", "I", "N", "T", "H", "E", "L", "O", "N", "I", "A", "F", "T", "E", "R", "N", "O", "O", "N", "T", "J", "C"], 5)
        self.addRow(tkLayout, ["G", "S", "I", "P", "B", "O", "M", "O", "R", "N", "I", "N", "G", "Q", "Z", "F", "U", "P", "G", "B", "F", "O", "T", "H"], 6)
        self.addRow(tkLayout, ["E", "V", "E", "N", "I", "N", "G", "N", "M", "O", "V", "E", "A", "X", "Z", "X", "M", "I", "D", "N", "I", "G", "H", "T"], 7)

        btnClose = QPushButton(text="Close", parent=self)
        btnClose.clicked.connect(self.close)

        ButtonLayout.addWidget(btnClose)

        centralLayout.addWidget(tkGroup)
        centralLayout.addLayout(ButtonLayout)

        centralWidget.setLayout(centralLayout)

        #  Set up short timer to update the clock every second
        self.Timer = QTimer(self)
        self.Timer.timeout.connect(self.updateTime)
        self.Timer.start(1000)

    def buildStatusBar(self):
        """  Create a status bar
        """
        self.statusBar = self.statusBar()
        self.statusBar.setSizeGripEnabled(False)

        self.stsDate    = QLabel("Thursday 23 October 2025")
        self.stsBattery = QProgressBar()
        self.stsState   = QLabel("cisN")
        self.stsIdle    = QLabel("idle : 7s")

        self.stsDate.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.stsBattery.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stsState.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stsIdle.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.statusBar.addPermanentWidget(self.stsDate,  1)
        self.statusBar.addPermanentWidget(self.stsBattery,  1)
        self.statusBar.addPermanentWidget(self.stsState, 1)
        self.statusBar.addPermanentWidget(self.stsIdle,  1)

        #self.stsBattery.setGeometry(0, 0, 8, 1)
        self.stsBattery.setFixedHeight(14)
        self.stsBattery.setFixedWidth(100)
        self.stsBattery.adjustSize()
    # ----------------------------------------------------------------------------------------------------------------------- addRow() --------------
    def addRow(self, layout, row, rowCount):
        column = 0
        for element in row:
            label = QLabel(element)
            name = f"{column}:{rowCount}"
            label.setObjectName(name)
            #label.setFixedWidth(self.size)
            label.adjustSize()
            label.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            layout.addWidget(label, rowCount, column)
            column += 1
    # ----------------------------------------------------------------------------------------------------------------------- updateTime() ----------
    def updateTime(self):
        """  Update the time and status bar every second.
        """
        dtCurrent = QDateTime.currentDateTime()
        txtDate   = dtCurrent.toString("dddd dd MMMM yyyy")

        self.stsDate.setText(txtDate)
        self.stsState.setText(f"{utils.getState()}")
        self.stsIdle.setText(utils.getIdleDuration())

        self.updateBattery()
    # ----------------------------------------------------------------------------------------------------------------------- updateBattery() -------
    def updateBattery(self):
        """  Updates the battery icon in the status bar.

             The colour of the progress bar indicated the state of the battery.

             Running on mains      - light blue.
             battery low           - red
             Running on Battery    - yellow
             Battery charging      - blue
             Battery fully charged - green

        """
        state  = self.systemInfo.onBattery
        charge = self.systemInfo.batteryCharge

        match state:
            case True:
                if charge == 100:                           #  Fully Charged
                    self.stsBattery.setValue(charge)
                    self.stsBattery.setStyleSheet(self.styles.BATTERY_FULL_STYLE)
                else:                                       #  Battery charging
                    self.stsBattery.setValue(charge)
                    self.stsBattery.setStyleSheet(self.styles.CHARGING_STYLE)
            case False:                                     #  Running on battery
                self.stsBattery.setValue(charge)
                if charge < 10:
                        self.stsBattery.setStyleSheet(self.styles.BATTERY_LOW_STYLE)
                else:
                    self.stsBattery.setStyleSheet(self.styles.RUNNING_ON_BATTERY_STYLE)
            case _:
                self.stsBattery.setStyleSheet(self.styles.RUNNING_ON_AC_STYLE)
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        self.parent.show()
        event.accept()
    # ----------------------------------------------------------------------------------------------------------------------- allOn() ---------------
    def allOn(self):
        """  Switches all the test element on.
        """
        tkc.it(self, "ON")
        tkc.iss(self, "ON")
        tkc.half(self, "ON")
        tkc.quarter(self, "ON")
        tkc.one(self, "ON")
        tkc.two(self, "ON")
        tkc.three(self, "ON")
        tkc.four(self, "ON")
        tkc.five(self, "ON")
        tkc.six(self, "ON")
        tkc.seven(self, "ON")
        tkc.eight(self, "ON")
        tkc.nine(self, "ON")
        tkc.ten(self, "ON")
        tkc.eleven(self, "ON")
        tkc.twelve(self, "ON")
        tkc.inn(self, "ON")
        tkc.the(self, "ON")
        tkc.on(self, "ON")
        tkc.after(self, "ON")
        tkc.noon(self, "ON")
        tkc.morning(self, "ON")
        tkc.evening(self, "ON")
        tkc.midnight(self, "ON")
    # ----------------------------------------------------------------------------------------------------------------------- allOff() --------------
    def allOff(self):
        """  Switches all the test element off.
        """
        tkc.it(self, "OFF")
        tkc.iss(self, "OFF")
        tkc.half(self, "OFF")
        tkc.quarter(self, "OFF")
        tkc.one(self, "OFF")
        tkc.two(self, "OFF")
        tkc.three(self, "OFF")
        tkc.four(self, "OFF")
        tkc.five(self, "OFF")
        tkc.six(self, "OFF")
        tkc.seven(self, "OFF")
        tkc.eight(self, "OFF")
        tkc.nine(self, "OFF")
        tkc.ten(self, "OFF")
        tkc.eleven("OFF")
        tkc.twelve(self, "OFF")
        tkc.inn(self, "OFF")
        tkc.the(self, "OFF")
        tkc.on(self, "OFF")
        tkc.after(self, "OFF")
        tkc.noon(self, "OFF")
        tkc.morning(self, "OFF")
        tkc.evening(self, "OFF")
        tkc.midnight(self, "OFF")
 

