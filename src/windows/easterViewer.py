###############################################################################################################
#    easterViewer   Copyright (C) <2026>  <Kevin Scott>                                                       #
#                                                                                                             #
#    Display Easter dates for a given year.                                                                   #
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

import datetime

import src.utils.easterDates as ed 

from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow, QFrame, QApplication,
                            QGroupBox, QGridLayout, QLabel, QComboBox, QSpinBox)
from PyQt6.QtCore    import Qt

import src.classes.styles as styles

class easterViewer(QMainWindow):
    """  Display results from a NTP server in a separate window.
    """
    def __init__(self, myLogger, myConfig):
        super().__init__()

        self.logger = myLogger
        self.config = myConfig
        self.styles = styles.Styles()

        self.height      = 400
        self.width       = 400
        self.screenSize  = QApplication.primaryScreen().availableGeometry()
        self.xPos        = int((self.screenSize.width() / 2)  - (self.width / 2))
        self.yPos        = int((self.screenSize.height() / 2) - (self.height / 2))

        self.setGeometry(self.xPos, self.yPos, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("Easter Dates")

        self.buildGUI()
        self.update()

    def buildGUI(self):
        """  Build the GUI elements.
        """
        #  Create a central widget.
        self.centralWidget = QFrame()
        self.centralWidget.setStyleSheet("margin:0px; border:0px")
        self.setCentralWidget(self.centralWidget)
        self.centralLayout = QVBoxLayout()
        self.ButtonLayout  = QHBoxLayout()

        self.ntpGroup   = QGroupBox("Easter Dates")
        self.ntpLayout  = QGridLayout(self.ntpGroup)

        self.txtGoodFriday   = QLabel("Good Friday")
        self.lblGoodFriday   = QLabel("03 April 2026")
        self.txtEasterSunday = QLabel("Easter Sunday")
        self.lblEasterSunday = QLabel("05 April 2026")
        self.txtEasterMonday = QLabel("Easter Monday")
        self.lblEasterMonday = QLabel("06 April 2026")
        self.txtTypeOfEaster = QLabel("Type of Easter")
        self.cbTypeOfEaster  = QComboBox()

        self.txtYearOfEaster = QLabel("Year")
        self.sbYearOfEaster  = QSpinBox(self)

        self.cbTypeOfEaster.insertItems(3, ["Hebrew Calendar", "Julian Calendar", "Gregorian Calendar"])
        self.cbTypeOfEaster.setStyleSheet(self.styles.QComboBox_STYLE)
        self.cbTypeOfEaster.setCurrentIndex(2)

        self.sbYearOfEaster.setMinimum(1)
        self.sbYearOfEaster.setMaximum(3000)
        self.sbYearOfEaster.setValue(2026)
        #self.sbYearOfEaster.setStyleSheet(self.styles.QSpinBox_STYLE)

        self.cbTypeOfEaster.currentTextChanged.connect(self.update)
        self.sbYearOfEaster.valueChanged.connect(self.update)

        self.ntpLayout.addWidget(self.txtGoodFriday,   0, 0, Qt.AlignmentFlag.AlignCenter)
        self.ntpLayout.addWidget(self.lblGoodFriday,   0, 1, Qt.AlignmentFlag.AlignLeft)
        self.ntpLayout.addWidget(self.txtEasterSunday, 1, 0, Qt.AlignmentFlag.AlignCenter)
        self.ntpLayout.addWidget(self.lblEasterSunday, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.ntpLayout.addWidget(self.txtEasterMonday, 2, 0, Qt.AlignmentFlag.AlignCenter)
        self.ntpLayout.addWidget(self.lblEasterMonday, 2, 1, Qt.AlignmentFlag.AlignLeft)
        self.ntpLayout.addWidget(self.txtTypeOfEaster, 3, 0, Qt.AlignmentFlag.AlignCenter)
        self.ntpLayout.addWidget(self.cbTypeOfEaster,  3, 1, Qt.AlignmentFlag.AlignLeft)
        self.ntpLayout.addWidget(self.txtYearOfEaster, 5, 0, Qt.AlignmentFlag.AlignCenter)
        self.ntpLayout.addWidget(self.sbYearOfEaster,  5, 1, Qt.AlignmentFlag.AlignLeft)

        self.ntpGroup.setStyleSheet(self.styles.QGroupBox_STYLE)
        self.ntpGroup.setLayout(self.ntpLayout)

        btnClose = QPushButton(text="Close", parent=self)
        btnClose.clicked.connect(self.close)

        self.ButtonLayout.addWidget(btnClose)

        self.centralLayout.addWidget(self.ntpGroup)
        self.centralLayout.addLayout(self.ButtonLayout)

        self.centralWidget.setLayout(self.centralLayout)

    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def update(self):
        """
        """
        match  self.cbTypeOfEaster.currentText():
            case "Hebrew Calendar":
                easterSunday = ed.hebrew_easter(self.sbYearOfEaster.value())
            case "Julian Calendar":
                easterSunday = ed.julian_easter(self.sbYearOfEaster.value())
            case "Gregorian Calendar":
                easterSunday = ed.gregorian_easter(self.sbYearOfEaster.value())

        easterMonday = easterSunday + datetime.timedelta(days=1)
        goodFriday   = easterSunday - datetime.timedelta(days=2)

        self.lblGoodFriday.setText(goodFriday.strftime("%d %B %Y"))
        self.lblEasterSunday.setText(easterSunday.strftime("%d %B %Y"))
        self.lblEasterMonday.setText(easterMonday.strftime("%d %B %Y"))
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        """  When the viewer is closed, checks if any child windows are still open.
        """
        event.accept()


