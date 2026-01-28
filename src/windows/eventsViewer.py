###############################################################################################################
#    eventsViewer   Copyright (C) <2026>  <Kevin Scott>                                                       #
#                                                                                                             #
#    Display Events in a table.                                                                               #
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

from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow, QFrame, QTableWidget,
                             QTableWidgetItem, QMessageBox, QApplication)

import src.classes.eventsStore as es
import src.windows.eventsAdd as ae

class EventsViewer(QMainWindow):
    """  Display friends in a table in a separate window.
    """
    def __init__(self, myLogger, myConfig):
        super().__init__()

        self.logger           = myLogger
        self.config           = myConfig
        self.eventsStore      = es.eventsStore(self, self.logger, self.config)
        self.events           = self.eventsStore.getEvents()
        self.eventsCategories = self.eventsStore.getCategories
        self.tableHeaders     = self.eventsStore.getHeaders
        self.noHeaders        = len(self.tableHeaders)
        self.eventsAdd        = None

        height     = 800
        width      = 800
        screenSize = QApplication.primaryScreen().availableGeometry()
        xPos       = int((screenSize.width() / 2)  - (width / 2))
        yPos       = int((screenSize.height() / 2) - (height / 2))

        self.setGeometry(xPos, yPos, 800, 800)
        self.setFixedSize(width, height)
        self.setWindowTitle("Events")

        self.buildGUI()
        self.loadTable()

    def buildGUI(self):
        """  Build the GUI elements.
        """
        #  Create a central widget.
        self.centralWidget = QFrame()
        self.centralWidget.setStyleSheet("margin:0px; border:0px")
        self.setCentralWidget(self.centralWidget)
        self.centralLayout = QVBoxLayout()
        self.ButtonLayout  = QHBoxLayout()

        self.tableView = QTableWidget()
        self.tableView.setColumnCount(self.noHeaders)
        self.tableView.setHorizontalHeaderLabels(self.tableHeaders)

        btnAdd = QPushButton(text="Add an Event", parent=self)
        btnAdd.clicked.connect(self.addEvent)

        btnEdit = QPushButton(text="Edit an Event", parent=self)
        btnEdit.clicked.connect(self.editEvent)

        btnDelete = QPushButton(text="Delete an Event", parent=self)
        btnDelete.clicked.connect(self.deleteEvent)

        btnRefresh = QPushButton(text="Refresh Events", parent=self)
        btnRefresh.clicked.connect(self.refreshEvents)

        btnClose = QPushButton(text="Close", parent=self)
        btnClose.clicked.connect(self.close)

        self.ButtonLayout.addWidget(btnAdd)
        self.ButtonLayout.addWidget(btnEdit)
        self.ButtonLayout.addWidget(btnDelete)
        self.ButtonLayout.addWidget(btnRefresh)
        self.ButtonLayout.addWidget(btnClose)

        self.centralLayout.addWidget(self.tableView)
        self.centralLayout.addLayout(self.ButtonLayout)

        self.centralWidget.setLayout(self.centralLayout)
    # ----------------------------------------------------------------------------------------------------------------------- loadTable() -----------
    def loadTable(self):
        """  Populate the table with events data.
             The finds data is a list of lists.
        """
        row = 0

        self.tableView.clear()
        self.tableView.setRowCount(row)
        self.tableView.setColumnCount(self.noHeaders)
        self.tableView.setHorizontalHeaderLabels(self.tableHeaders)

        for event in self.events:
            self.tableView.insertRow(row)
            col = 0
            for item in event:
                self.tableView.setItem(row, col, QTableWidgetItem(item))
                col += 1

            row += 1
    # ----------------------------------------------------------------------------------------------------------------------- addEvent() ------------
    def addEvent(self):
        """   Open the Add Events windows.
        """
        if self.eventsAdd is None:
            self.eventsAdd = ae.AddFriends(self.logger, self.eventsCategories, self.tableHeaders)     #  Needs to be self. - to keep window alive.
            self.eventsAdd.show()
            self.eventsAdd.addNewEvent.connect(self.addNewEvent)                                      #  Signal is fired when a friend is to be added.
            self.eventsAdd.closeNewEvent.connect(self.closeNewEvent)                                     #  Signal is fired when the addFriend window is closed.
    # ----------------------------------------------------------------------------------------------------------------------- addNewFriend() --------
    def addNewEvent(self,event):
        """  Adds a new Event to the events store.
             The events store is then re-loaded, this ensures the data is sorted.
             LoadTable is called to refresh the displayed data.
        """
        key  = event[1]
        item = event
        self.eventsStore.addEvent(key, item)
        self.refreshEvents()
    # ----------------------------------------------------------------------------------------------------------------------- editEvent() -----------
    def editEvent(self):
        pass
    # ----------------------------------------------------------------------------------------------------------------------- deleteFriend() --------
    def deleteEvent(self):
        """  Deletes an event from the table.
             Displays an error if no row selected.
             Prompts user for confirmation.
        """
        row = self.tableView.currentRow()

        if row == -1:
            confirmation = QMessageBox.information(self, "Error.", "No row selected.")
            return

        name         = f"{self.tableView.item(row, 2).text()} {self.tableView.item(row, 1).text()}"
        confirmation = QMessageBox.question(self, "Confirmation", f"Delete an Event {name}")

        if confirmation == QMessageBox.StandardButton.Yes:
            key = f"{self.tableView.item(row, 0).text()}"
            print(key)
            self.eventsStore.deleteEvent(key)             #  Delete event
            self.refreshEvents()
    # ----------------------------------------------------------------------------------------------------------------------- refreshEvents() -------
    def refreshEvents(self):
        """  Save the table to the friends store, the friends store is then re-loaded into the table.
             Called when a friend has been added, deleted or edited.
        """
        self.eventsStore.saveEvents()
        self.events = self.eventsStore.getEvents()
        self.loadTable()
    # ----------------------------------------------------------------------------------------------------------------------- closeNewFriend() ------
    def closeNewEvent(self):
        """  When the newEvents window is closed, it signals here so the reference can be set to null.
        """
        self.eventsAdd = None
   # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        """  When the viewer is closed, checks if any child windows are still open.
        """
        if self.eventsAdd:
            confirmation = QMessageBox.question(self, "Confirmation", "The Add Event's Windows is still open - Continue?")

            if confirmation == QMessageBox.StandardButton.Yes:
                event.accept()      #  Close the app.
                self.eventsAdd.close()
            else:
                event.ignore()      #  Continue the app.


 
