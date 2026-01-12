###############################################################################################################
#    About   Copyright (C) <2025-26>  <Kevin Scott>                                                           #
#                                                                                                             #
#    Displays an about dialog.                                                                                #
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

from PyQt6.QtWidgets import (QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
                             QApplication, QFrame, QPushButton)
from PyQt6.QtCore    import Qt

class AddFriends(QMainWindow):
    def __init__(self, myLogger, titles):
        super().__init__()

        self.logger = myLogger
        self.titles = titles
        self.height = 400
        self.width  = 400
        screenSize  = QApplication.primaryScreen().availableGeometry()
        xPos        = int((screenSize.width() / 2)  - (self.width / 2))
        yPos        = int((screenSize.height() / 2) - (self.height / 2))

        self.logger.info("Launching Add Friends dialog")

        self.setWindowTitle("Add a Friend")
        self.setGeometry(xPos, yPos, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        self.buildGUI()

    def buildGUI(self):
        """  Build the GUI elements.
        """
        #  Create a central widget.
        self.centralWidget = QFrame()
        self.centralWidget.setStyleSheet("margin:0px; border:0px")
        self.setCentralWidget(self.centralWidget)
        self.centralLayout = QVBoxLayout()
        self.entryLayout   = QGridLayout()
        self.ButtonLayout  = QHBoxLayout()

        lblTitle      = QLabel("Title")
        cbTitle       = QComboBox()
        lblFirstName  = QLabel("First Name")
        lneFisstName  = QLineEdit("", self)
        lblSecondName = QLabel("Second Name")
        lneSecondName = QLineEdit("", self)
        lblMobileNo   = QLabel("Mobile Number")
        lneMobileNo   = QLineEdit("", self)
        lblTelNo      = QLabel("Telephone Number")
        lneTelNo      = QLineEdit("", self)
        lblEmail      = QLabel("E-Mail")
        lneEmail      = QLineEdit("", self)
        lblBirthday   = QLabel("Birthday")
        lblHouseNo    = QLabel("House No")
        lneHouseNo    = QLineEdit("", self)
        lblAddLine1   = QLabel("Address Line 1")
        lneAddLine1   = QLineEdit("", self)
        lblAddLine2   = QLabel("Address Line 1")
        lneAddLine2   = QLineEdit("", self)
        lblCity       = QLabel("City")
        lneCity       = QLineEdit("", self)
        lblCounty     = QLabel("County")
        lneCounty     = QLineEdit("", self)
        lblPostCode   = QLabel("Pose Code")
        lnePostCode   = QLineEdit("", self)
        lblCountry    = QLabel("Country")
        lneCountry    = QLineEdit("", self)
        lblNotes      = QLabel("Notes")
        lneNotes      = QLineEdit("", self)


        cbTitle.insertItems(0, self.titles)

        self.entryLayout.addWidget(lblTitle,     0, 0, Qt.AlignmentFlag.AlignCenter)
        self.entryLayout.addWidget(cbTitle,      0, 1, Qt.AlignmentFlag.AlignRight)
        self.entryLayout.addWidget(lblFirstName, 1, 0, Qt.AlignmentFlag.AlignCenter)
        self.entryLayout.addWidget(lneFisstName, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.entryLayout.addWidget(lblSecondName,1, 2, Qt.AlignmentFlag.AlignCenter)
        self.entryLayout.addWidget(lneSecondName,1, 3, Qt.AlignmentFlag.AlignRight)
        self.entryLayout.addWidget(lblMobileNo,  2, 0, Qt.AlignmentFlag.AlignCenter)
        self.entryLayout.addWidget(lneMobileNo,  2, 1, Qt.AlignmentFlag.AlignRight)
        self.entryLayout.addWidget(lblTelNo,     2, 2, Qt.AlignmentFlag.AlignCenter)
        self.entryLayout.addWidget(lneTelNo,     2, 3, Qt.AlignmentFlag.AlignRight)
        self.entryLayout.addWidget(lblEmail,     3, 0, Qt.AlignmentFlag.AlignCenter)
        self.entryLayout.addWidget(lneEmail,     3, 1, Qt.AlignmentFlag.AlignRight)
        self.entryLayout.addWidget(lblBirthday,  3, 2, Qt.AlignmentFlag.AlignCenter)
        self.entryLayout.addWidget(lblHouseNo,   4, 0, Qt.AlignmentFlag.AlignRight)
        self.entryLayout.addWidget(lneHouseNo,   4, 1, Qt.AlignmentFlag.AlignCenter)
        self.entryLayout.addWidget(lblAddLine1,  5, 0, Qt.AlignmentFlag.AlignCenter)
        self.entryLayout.addWidget(lneAddLine1,  5, 1, Qt.AlignmentFlag.AlignRight)
        self.entryLayout.addWidget(lblAddLine2,  5, 2, Qt.AlignmentFlag.AlignCenter)
        self.entryLayout.addWidget(lneAddLine2,  5, 3, Qt.AlignmentFlag.AlignRight)
        self.entryLayout.addWidget(lblCity,      6, 0, Qt.AlignmentFlag.AlignCenter)
        self.entryLayout.addWidget(lneCity,      6, 1, Qt.AlignmentFlag.AlignRight)
        self.entryLayout.addWidget(lblCounty,    6, 2, Qt.AlignmentFlag.AlignCenter)
        self.entryLayout.addWidget(lneCounty,    6, 3, Qt.AlignmentFlag.AlignRight)
        self.entryLayout.addWidget(lblPostCode,  7, 0, Qt.AlignmentFlag.AlignCenter)
        self.entryLayout.addWidget(lnePostCode,  7, 1, Qt.AlignmentFlag.AlignRight)
        self.entryLayout.addWidget(lblCountry,   7, 2, Qt.AlignmentFlag.AlignCenter)
        self.entryLayout.addWidget(lneCountry,   7, 3, Qt.AlignmentFlag.AlignRight)
        self.entryLayout.addWidget(lblNotes,     8, 0, Qt.AlignmentFlag.AlignCenter)
        self.entryLayout.addWidget(lneNotes,     8, 1, Qt.AlignmentFlag.AlignRight)

        btnAdd = QPushButton(text="Add a Friend", parent=self)
        btnAdd.clicked.connect(self.addFriend)

        btnExit = QPushButton(text="Exit - No Save", parent=self)
        btnExit.clicked.connect(self.close)

        self.ButtonLayout.addWidget(btnAdd)
        self.ButtonLayout.addWidget(btnExit)

        self.centralLayout.addLayout(self.entryLayout)
        self.centralLayout.addLayout(self.ButtonLayout)
        self.centralWidget.setLayout(self.centralLayout)


    def addFriend(self):
        pass


    def closeEvent(self, event):
        self.logger.info("Add Friends Close Event")
        event.accept()


