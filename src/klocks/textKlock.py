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
from PyQt6.QtCore    import Qt, QSize

import src.classes.styles as styles
import src.classes.systemInfo as si

import src.utils.textKlockCodes as tkc
import src.utils.klock_utils as utils


class textKlock(QMainWindow):
    """  A class that displays the time within a matrix of words.
    """
    def __init__(self, myConfig, parent):
        super().__init__()

        self.config      = myConfig
        self.styles      = styles.Styles()             #  Styles for the battery progress bar.
        self.systemInfo  = si.SysInfo()
        self.parent      = parent
        self.onColour    = self.config.TK_ON_COLOUR
        self.offColour   = self.config.TK_OFF_COLOUR
        self.backColour  = self.config.TK_BACKGROUND
        self.transparent = self.config.TK_TRANSPARENT

        self.parent.hide()

        if self.transparent:
            print("Transparent")
            self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            self.setStyleSheet("background : transparent;")
        else:
            print("Not Transparent")
            self.setStyleSheet("background : {self.backColour};")

        height     = 500
        width      = 300
        screenSize = QApplication.primaryScreen().availableGeometry()
        xPos       = int((screenSize.width() / 2)  - (width / 2))
        yPos       = int((screenSize.height() / 2) - (height / 2))

        self.setGeometry(xPos, yPos, height, width)
        self.setWindowTitle("pyKlock")

        self.buildGUI()
        self.buildStatusBar()

        self.updateTime()
        
    def buildGUI(self):
        """  Build the GUI elements.
        """
        centralWidget = QFrame()
        self.setCentralWidget(centralWidget)
        centralLayout = QVBoxLayout()
        ButtonLayout  = QHBoxLayout()

        tkGroup  = QGroupBox("Text Klock")
        tkLayout = QGridLayout(tkGroup)
        
        tkLayout.setColumnMinimumWidth(0, 8)
        tkLayout.setColumnMinimumWidth(1, 8)
        tkLayout.setColumnMinimumWidth(2, 8)

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
            hint = QSize(10, 10)
            label.setFixedSize(hint)
            label.adjustSize()
            label.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            layout.addWidget(label, rowCount, column, Qt.AlignmentFlag.AlignCenter)
            column += 1
    # ----------------------------------------------------------------------------------------------------------------------- updateTime() ----------
    def updateTime(self):
        """  Update the time and status bar every second.
        """
        dtCurrent = QDateTime.currentDateTime()
        txtDate   = dtCurrent.toString("dddd dd MMMM yyyy")
        txtTime   = dtCurrent.toString("HH:mm:ss")
        hours     = int(txtTime[0:2])
        minutes   = int(txtTime[3:5])

        tkc.allOff(self)           #  Switch all text elements off.
        self.setHours(hours, minutes)
        self.setMinutes(minutes)

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
    # ----------------------------------------------------------------------------------------------------------------------- setHours() ------------
    def setHours(self, hours, minutes):
        """  Switches on the appropriate text to display the hour.
        """
        tkc.it(self, "ON")
        tkc.iss(self, "ON")
        tkc.inn(self, "ON")
        tkc.the(self, "ON")

        if minutes > 30:     #  Increment hours if time is close to the hour.
            hours += 1

        match hours:
            case 0 | 24:
                if minutes in [58, 59, 0, 1]:
                    tkc.midnight(self, "ON")
                else:
                    tkc.twelve(self, "ON")
                    if minutes > 30:
                        tkc.evening(self, "ON")
                    else:
                        tkc.morning(self, "ON")
            case 1:
                tkc.one(self, "ON")
                tkc.morning(self, "ON")
            case 2:
                tkc.two(self, "ON")
                tkc.morning(self, "ON")
            case 3:
                tkc.three(self, "ON")
                tkc.morning(self, "ON")
            case 4:
                tkc.four(self, "ON")
                tkc.morning(self, "ON")
            case 5:
                tkc.fiveHour(self, "ON")
                tkc.morning(self, "ON")
            case 6:
                tkc.six(self, "ON")
                tkc.morning(self, "ON")
            case 7:
                tkc.seven(self, "ON")
                tkc.morning(self, "ON")
            case 8:
                tkc.eight(self, "ON")
                tkc.morning(self, "ON")
            case 9:
                tkc.nine(self, "ON")
                tkc.morning(self, "ON")
            case 10:
                tkc.tenHour(self, "ON")
                tkc.morning(self, "ON")
            case 11:
                tkc.eleven(self, "ON")
                tkc.morning(self, "ON")
            case 12:
                if minutes in [58, 59, 0, 1]:
                    tkc.noon(self, "ON")
                else:
                    self.twelve(self, "ON")
                    if minutes > 30:
                        tkc.morning(self, "ON")
                    else:
                        tkc.after(self, "ON")
                        tkc.noon(self, "ON")
            case 13:
                tkc.one(self, "ON")
                tkc.after(self, "ON")
                tkc.noon(self, "ON")
            case 14:
                tkc.two(self, "ON")
                tkc.after(self, "ON")
                tkc.noon(self, "ON")
            case 15:
                tkc.three(self, "ON")
                tkc.after(self, "ON")
                tkc.noon(self, "ON")
            case 16:
                tkc.four(self, "ON")
                tkc.after(self, "ON")
                tkc.noon(self, "ON")
            case 17:
                tkc.fiveHour(self, "ON")
                tkc.after(self, "ON")
                tkc.noon(self, "ON")
            case 18:
                tkc.six(self, "ON")
                tkc.evening(self, "ON")
            case 19:
                tkc.seven(self, "ON")
                tkc.after(self, "ON")
                tkc.noon(self, "ON")
            case 20:
                tkc.eight(self, "ON")
                tkc.evening(self, "ON")
            case 21:
                tkc.nine(self, "ON")
                tkc.evening(self, "ON")
            case 22:
                tkc.tenHour(self, "ON")
                tkc.evening(self, "ON")
            case 23:
                tkc.eleven(self, "ON")
                tkc.evening(self, "ON")
    # ----------------------------------------------------------------------------------------------------------------------- setMinutes() ----------
    def setMinutes(self, minutes):
        """  Switches on the appropriate text to display the minutes.
        """
        if minutes > 30:
            minutes = 60 - minutes
            tkc.to(self, "ON")
        else:
            tkc.past(self, "ON")

        match minutes:
            case minutes if (0 <= minutes <= 2):
                tkc.to(self, "OFF")
                tkc.past(self, "OFF")
            case minutes if (2 < minutes <= 7):
                tkc.fiveMinute(self, "ON")
            case minutes if (7 < minutes <= 12):
                tkc.tenMinute(self, "ON")
            case minutes if (13 < minutes <= 17):
                tkc.a(self, "ON")
                tkc.quarter(self, "ON")
            case minutes if (17 < minutes <= 22):
                tkc.twenty(self, "ON")
            case minutes if (22 < minutes <= 27):
                tkc.twenty(self, "ON")
                tkc.fiveMinute(self, "ON")
            case minutes if (27 < minutes <= 30):
                tkc.to(self, "OFF")
                tkc.past(self, "ON")
                tkc.half(self, "ON")

    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        self.parent.show()
        event.accept()

 

