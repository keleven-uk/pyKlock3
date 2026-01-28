###############################################################################################################
#    eventsAdd   Copyright (C) <2026>  <Kevin Scott>                                                          #
#                                                                                                             #
#    Displays an Events add window.                                                                           #
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
                             QApplication, QFrame, QPushButton, QPlainTextEdit, QDateEdit, QMessageBox, 
                             QTimeEdit)
from PyQt6.QtCore    import Qt, pyqtSignal, QDate, QTime

from src.classes.QToggle import QToggle

import src.classes.styles as styles

class AddFriends(QMainWindow):
    """  Displays a window, so that a new Event data can be entered.
    """

    addNewEvent   = pyqtSignal(list)  # <-- This is the sub window's signal
    closeNewEvent = pyqtSignal()      # <-- This is the sub window's signal

    def __init__(self, myLogger, categories, headers):
        super().__init__()

        self.logger     = myLogger
        self.styles     = styles.Styles()
        self.categories = categories
        self.headers    = headers
        self.today      = QDate.currentDate()
        self.newEvent   = ["", self.today.toString("d MMMM yyyy"), "00:00", "", "", "", "", "", "", ""]
        self.height     = 400
        self.width      = 600
        self.leWidth    = 150                #  Width of a line edit
        screenSize      = QApplication.primaryScreen().availableGeometry()
        xPos            = int((screenSize.width() / 2)  - (self.width / 2))
        yPos            = int((screenSize.height() / 2) - (self.height / 2))

        self.logger.info("Launching Add Friends dialog")

        self.setWindowTitle("Add a Friend")
        self.setGeometry(xPos, yPos, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        self.buildGUI()

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

        lblName = QLabel("Event Name")
        lneName = QLineEdit("", self)
        lneName.setObjectName("Event Name")
        lneName.editingFinished.connect(self.addElement)
        lneName.setFixedWidth(self.leWidth)
        entryLayout.addWidget(lblName, 0, 0, Qt.AlignmentFlag.AlignCenter)
        entryLayout.addWidget(lneName, 0, 1, Qt.AlignmentFlag.AlignCenter)

        lblCategory = QLabel("Category")
        cbCategory  = QComboBox()
        cbCategory.setObjectName("Category")
        cbCategory.insertItems(0, self.categories)
        cbCategory.currentTextChanged.connect(self.addElement)
        cbCategory.setStyleSheet(self.styles.QComboBox_STYLE)
        entryLayout.addWidget(lblCategory, 0, 2, Qt.AlignmentFlag.AlignCenter)
        entryLayout.addWidget(cbCategory,  0, 3, Qt.AlignmentFlag.AlignCenter)

        lblDateDue = QLabel("Date Due")
        dteDateDue = QDateEdit(self, calendarPopup=True)
        dteDateDue.setDisplayFormat("d-MMMM-yyyy")
        dteDateDue.setDate(self.today)
        dteDateDue.setObjectName("Date Due")
        dteDateDue.dateTimeChanged.connect(self.addElement)
        dteDateDue.setStyleSheet(self.styles.QDateEdit_STYLE)
        dteDateDue.setTime(QTime(0, 0))
        entryLayout.addWidget(lblDateDue, 1, 0, Qt.AlignmentFlag.AlignCenter)
        entryLayout.addWidget(dteDateDue, 1, 1, Qt.AlignmentFlag.AlignCenter)

        lblTimeDue = QLabel("Time Due")
        teTimeDue  = QTimeEdit(self)
        teTimeDue.setDisplayFormat("HH-MM")
        teTimeDue.setTime(QTime.currentTime())  
        teTimeDue.setObjectName("Time Due")
        teTimeDue.editingFinished.connect(self.addElement)
        teTimeDue.setDisplayFormat("HH:mm")
        teTimeDue.setTime(QTime(0, 0))
        teTimeDue.setStyleSheet(self.styles.QTimeEdit_STYLE)
        entryLayout.addWidget(lblTimeDue, 1, 2, Qt.AlignmentFlag.AlignCenter)
        entryLayout.addWidget(teTimeDue, 1, 3, Qt.AlignmentFlag.AlignCenter)

        lblRecurring = QLabel("Recurring")
        tgRecurring  = QToggle(self)
        tgRecurring.setChecked(False)
        tgRecurring.stateChanged.connect(self.addElement)
        tgRecurring.setObjectName("Recurring")
        tgRecurring.setStyleSheet(self.styles.QToggle_STYLE)
        entryLayout.addWidget(lblRecurring, 2, 0, Qt.AlignmentFlag.AlignCenter)
        entryLayout.addWidget(tgRecurring,  2, 1, Qt.AlignmentFlag.AlignCenter)

        lblNotes = QLabel("Notes")
        lteNotes = QPlainTextEdit("", self)
        lteNotes.setObjectName("Notes")
        lteNotes.textChanged.connect(self.addElement)
        entryLayout.addWidget(lblNotes, 3, 0, Qt.AlignmentFlag.AlignCenter)
        entryLayout.addWidget(lteNotes, 3, 1, 3, 3)

        self.btnAdd = QPushButton(text="Add a Friend", parent=self)
        self.btnAdd.setEnabled(False)
        self.btnAdd.clicked.connect(self.addEvent)

        btnExit = QPushButton(text="Exit - No Save", parent=self)
        btnExit.clicked.connect(self.close)

        ButtonLayout.addWidget(self.btnAdd)
        ButtonLayout.addWidget(btnExit)

        centralLayout.addLayout(entryLayout)
        centralLayout.addLayout(ButtonLayout)
        centralWidget.setLayout(centralLayout)
    # ----------------------------------------------------------------------------------------------------------------------- addElement() ----------
    def addElement(self):
        """  When an element has been edited, add the data to the appropriate position in the new event list.
             We replace instead of inserting, to stop the list growing.
        """
        action    = self.sender()
        name      = action.objectName()

        match name:
            case "Event Name":
                self.newEvent[0] = action.text().title().strip()
                self.addEventValidate()
            case "Date Due":
                self.newEvent[1] = action.date().toString("d MMMM yyyy")
                self.addEventValidate()
            case "Time Due":
                self.newEvent[2] = str(action.time().toPyTime())
            case "Category":
                self.newEvent[3] = action.currentText()
            case "Recurring":
                self.newEvent[4] = ""
            case "Notes":
                self.newEvent[5] = action.toPlainText()
    # ----------------------------------------------------------------------------------------------------------------------- addEventValidate() ----
    def addEventValidate(self):
        """  Event name and Event category are mandatory.
        """
        if self.newEvent[0] and self.newEvent[1]:
            self.btnAdd.setEnabled(True)
    # ----------------------------------------------------------------------------------------------------------------------- addEvent() ------------
    def addEvent(self, event):
        print(self.newEvent)
        """  Checks is there is new data, if so, signals the parent and passes the data.

             Will only emit the signal if their is a Event Name and Event category.
        """
        if self.newEvent == []:
            self.close()
        else:
            if self.newEvent[0] and self.newEvent[1]:
                self.addNewEvent.emit(self.newEvent)      #  emit signal
                self.close()
            else:
                QMessageBox.information(self, "Error on data entry.", "Event Name and Event category are mandatory.")
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        """  Closes the window and informs the parent.
        """
        self.logger.info("Add Events Close Event")
        self.closeNewEvent.emit()                          #  emit signal
        event.accept()


