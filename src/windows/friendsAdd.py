###############################################################################################################
#    friendsAdd   Copyright (C) <2026>  <Kevin Scott>                                                         #
#                                                                                                             #
#    Displays an friends add window.                                                                          #
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

from titlecase import titlecase

from PyQt6.QtWidgets import (QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
                             QApplication, QFrame, QPushButton, QPlainTextEdit, QDateEdit, QMessageBox)
from PyQt6.QtCore    import Qt, pyqtSignal, QDate

import src.classes.styles as styles

class AddFriends(QMainWindow):
    """  Displays a window, so that a new friends data can be entered in add mode.
         If a friend is supplied, then enter edit mode and display the data.
    """

    addNewFriend   = pyqtSignal(list)  # <-- This is the sub window's signal
    closeNewFriend = pyqtSignal()      # <-- This is the sub window's signal

    def __init__(self, myLogger, titles, headers, friend=None):
        super().__init__()

        self.logger    = myLogger
        self.styles    = styles.Styles()
        self.titles    = titles
        self.headers   = headers
        self.newFriend = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        self.friend    = friend
        self.height    = 400
        self.width     = 600
        self.leWidth   = 150                #  Width of a line edit
        screenSize     = QApplication.primaryScreen().availableGeometry()
        xPos           = int((screenSize.width() / 2)  - (self.width / 2))
        yPos           = int((screenSize.height() / 2) - (self.height / 2))

        self.logger.info("Launching Add Friends dialog")

        self.setWindowTitle("Add a Friend")
        self.setGeometry(xPos, yPos, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        self.buildGUI()

        if self.friend:
            self.PopulateFriend()
            self.btnAdd.setText("Save Edited Friend")
            self.btnAdd.setEnabled(True)

    def buildGUI(self):
        """  Build the GUI elements.
        """
        #  Create a central widget.
        centralWidget = QFrame()
        centralWidget.setStyleSheet("margin:0px; border:0px")
        self.setCentralWidget(centralWidget)
        centralLayout = QVBoxLayout()
        entryLayout   = QGridLayout()
        ButtonLayout  = QHBoxLayout()

        row = 0
        col = 0

        for header in self.headers:
            match header:
                case "Title":
                    self.lblElement = QLabel(header)
                    self.cbElement  = QComboBox()
                    self.cbElement.setObjectName(header)
                    self.cbElement.insertItems(0, self.titles)
                    self.cbElement.currentTextChanged.connect(self.addElement)
                    entryLayout.addWidget(self.lblElement, row, col, Qt.AlignmentFlag.AlignCenter)
                    entryLayout.addWidget(self.cbElement,  row, col+1, Qt.AlignmentFlag.AlignRight)
                    row += 1
                case "First Name" | "Last Name" | "Mobile Number" | "Telephone Number" | "E-Mail" | "Address Line 1" | "Address Line 2" | \
                     "City" | "County" | "Post Code" | "Country":
                    cell = entryLayout.itemAtPosition(row, 0)
                    if cell:                #  If column is in use, set column number to 2 and add as row.
                        nextRow = row + 1
                        col = 2
                    else:
                        nextRow = row

                    self.lblElement = QLabel(header)
                    self.lneElement = QLineEdit("", self)
                    self.lneElement.setObjectName(header)
                    self.lneElement.editingFinished.connect(self.addElement)
                    self.lneElement.setFixedWidth(self.leWidth)
                    entryLayout.addWidget(self.lblElement, row, col, Qt.AlignmentFlag.AlignCenter)
                    entryLayout.addWidget(self.lneElement, row, col+1, Qt.AlignmentFlag.AlignCenter)
                    row = nextRow           #  Pass on the added row.
                case "House Number":
                    self.lblElement = QLabel(header)
                    self.lneElement = QLineEdit("", self)
                    self.lneElement.setObjectName(header)
                    self.lneElement.setFixedWidth(self.leWidth)
                    self.lneElement.editingFinished.connect(self.addElement)
                    entryLayout.addWidget(self.lblElement, row, col, Qt.AlignmentFlag.AlignCenter)
                    entryLayout.addWidget(self.lneElement, row, col+1, Qt.AlignmentFlag.AlignCenter)
                    row += 1
                case "Birthday":
                    self.lblElement = QLabel(header)
                    self.dteElement = QDateEdit(self, calendarPopup=True)
                    self.dteElement.setDisplayFormat("d-MMMM-yyyy")
                    self.dteElement.setDate(QDate.currentDate())
                    self.dteElement.setObjectName(header)
                    self.dteElement.dateTimeChanged.connect(self.addElement)
                    self.dteElement.setStyleSheet(self.styles.QDateEdit_STYLE)
                    entryLayout.addWidget(self.lblElement, row, 2, Qt.AlignmentFlag.AlignCenter)
                    entryLayout.addWidget(self.dteElement, row, 3, Qt.AlignmentFlag.AlignCenter)

                    row += 1
                case "Notes":
                    self.lblElement = QLabel(header)
                    self.lteElement = QPlainTextEdit("", self)
                    self.lteElement.setObjectName(header)
                    self.lteElement.textChanged.connect(self.addElement)
                    entryLayout.addWidget(self.lblElement, row, col, Qt.AlignmentFlag.AlignCenter)
                    entryLayout.addWidget(self.lteElement, row, col+1, 3, 3)


            col = 0     #  Reset column number.

        self.btnAdd = QPushButton(text="Add a Friend", parent=self)
        self.btnAdd.setEnabled(False)
        self.btnAdd.clicked.connect(self.addFriend)

        btnExit = QPushButton(text="Exit - No Save", parent=self)
        btnExit.clicked.connect(self.close)

        ButtonLayout.addWidget(self.btnAdd)
        ButtonLayout.addWidget(btnExit)

        centralLayout.addLayout(entryLayout)
        centralLayout.addLayout(ButtonLayout)
        centralWidget.setLayout(centralLayout)
    # ----------------------------------------------------------------------------------------------------------------------- PopulateFriend() ------
    def PopulateFriend(self):
        """  If in edit mode, populate the friends with friends data.
        """
        element = self.findChild(QComboBox, "Title")
        index   = element.findText(self.friend[0])
        element.setCurrentIndex(index)
        element = self.findChild(QLineEdit, "Last Name")
        element.setText(self.friend[1])
        element = self.findChild(QLineEdit, "First Name")
        element.setText(self.friend[2])
        element = self.findChild(QLineEdit, "Mobile Number")
        element.setText(self.friend[3])
        element = self.findChild(QLineEdit, "Telephone Number")
        element.setText(self.friend[4])
        element = self.findChild(QLineEdit, "E-Mail")
        element.setText(self.friend[5])
        element = self.findChild(QDateEdit, "Birthday")
        birthday = QDate.fromString(self.friend[6], "d MMMM yyyy")
        element.setDate(birthday)
        element = self.findChild(QLineEdit, "House Number")
        element.setText(self.friend[7])
        element = self.findChild(QLineEdit, "Address Line 1")
        element.setText(self.friend[8])
        element = self.findChild(QLineEdit, "Address Line 2")
        element.setText(self.friend[9])
        element = self.findChild(QLineEdit, "City")
        element.setText(self.friend[10])
        element = self.findChild(QLineEdit, "County")
        element.setText(self.friend[11])
        element = self.findChild(QLineEdit, "Post Code")
        element.setText(self.friend[12])
        element = self.findChild(QLineEdit, "Country")
        element.setText(self.friend[13])
        element = self.findChild(QPlainTextEdit, "Notes")
        element.setPlainText(self.friend[14])

    # ----------------------------------------------------------------------------------------------------------------------- addElement() ----------
    def addElement(self):
        """  When an element has been edited, add the data to the appropriate position in the new friends list.
             We replace instead of inserting, to stop the list growing.
        """
        action    = self.sender()
        name      = action.objectName()

        match name:
            case "Title":
                self.newFriend[0] = action.currentText()
            case "First Name":
                self.newFriend[2] = titlecase(action.text().strip())  
                self.addFriendValidate()
            case "Last Name":
                self.newFriend[1] = titlecase(action.text().strip())
                self.addFriendValidate()
            case "Mobile Number":
                self.newFriend[3] = action.text()
            case "Telephone Number":
                self.newFriend[4] = action.text()
            case "E-Mail" :
                self.newFriend[5] = action.text()
            case "Birthday":
                self.newFriend[6] = action.date().toString("d MMMM yyyy")
            case "House Number":
                self.newFriend[7] = action.text()
            case "Address Line 1":
                self.newFriend[8] = titlecase(action.text().strip())  
            case "Address Line 2":
                self.newFriend[9] = titlecase(action.text().strip())   
            case "City":
                self.newFriend[10] = titlecase(action.text().strip())  
            case "County":
                self.newFriend[11] = titlecase(action.text().strip())  
            case "Post Code":
                self.newFriend[12] = action.text()
            case "Country":
                self.newFriend[13] = titlecase(action.text().strip()) 
            case "Notes":
                self.newFriend[14] = action.toPlainText()
    # ----------------------------------------------------------------------------------------------------------------------- addFriendValidate() ---
    def addFriendValidate(self):
        """  First name and Last Name are mandatory.
        """
        if self.newFriend[1] and self.newFriend[2]:
            self.btnAdd.setEnabled(True)
    # ----------------------------------------------------------------------------------------------------------------------- addFriend() -----------
    def addFriend(self):
        """  Checks is there is new data, if so, signals the parent and passes the data.

             Will only emit the signal if their is a First name and a Last Name.
        """
        if self.newFriend == []:
            self.close()
        else:
            if self.newFriend[1] and self.newFriend[2]:
                self.addNewFriend.emit(self.newFriend)      #  emit signal
                self.close()
            else:
                QMessageBox.information(self, "Error on data entry.", "First Name and last name are mandatory.")
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        """  Closes the window and informs the parent.
        """
        self.logger.info("Add Friends Close Event")
        self.closeNewFriend.emit()                          #  emit signal
        event.accept()


