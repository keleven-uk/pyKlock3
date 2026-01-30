###############################################################################################################
#    friendsViewer   Copyright (C) <2025-26>  <Kevin Scott>                                                   #
#                                                                                                             #
#    Display friends in a table.                                                                              #
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

import src.classes.friendsStore as fs
import src.windows.friendsAdd as af

class FriendsViewer(QMainWindow):
    """  Display friends in a table in a separate window.
    """
    def __init__(self, myLogger):
        super().__init__()

        self.logger        = myLogger
        self.friendsStore  = fs.friendsStore(self.logger)
        self.friends       = self.friendsStore.getFriends()
        self.friendsTitles = self.friendsStore.getTitles
        self.tableHeaders  = self.friendsStore.getHeaders
        self.noHeaders     = len(self.tableHeaders)
        self.friendsAdd    = None

        height     = 800
        width      = 1500
        screenSize = QApplication.primaryScreen().availableGeometry()
        xPos       = int((screenSize.width() / 2)  - (width / 2))
        yPos       = int((screenSize.height() / 2) - (height / 2))

        self.setGeometry(xPos, yPos, height, width)
        self.setFixedSize(width, height)
        self.setWindowTitle("Friends")

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

        btnAdd = QPushButton(text="Add a Friend", parent=self)
        btnAdd.clicked.connect(self.addFriend)

        btnEdit = QPushButton(text="Edit a Friend", parent=self)
        btnEdit.clicked.connect(self.editFriend)

        btnDelete = QPushButton(text="Delete a Friend", parent=self)
        btnDelete.clicked.connect(self.deleteFriend)

        btnRefresh = QPushButton(text="Refresh Friends", parent=self)
        btnRefresh.clicked.connect(self.refreshFriends)

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
        """  Populate the table with friends data.
             The finds data is a list of lists.
        """
        row = 0

        self.tableView.clear()
        self.tableView.setRowCount(row)
        self.tableView.setColumnCount(self.noHeaders)
        self.tableView.setHorizontalHeaderLabels(self.tableHeaders)

        for friend in self.friends:
            self.tableView.insertRow(row)
            col = 0
            for item in friend:
                self.tableView.setItem(row, col, QTableWidgetItem(item))
                col += 1

            row += 1
            
        for head in range(self.noHeaders):
            self.tableView.resizeColumnToContents(head)
    # ----------------------------------------------------------------------------------------------------------------------- loadTable() -----------
    def addFriend(self):
        """   Open the Add Friends windows.
        """
        if self.friendsAdd is None:
            self.friendsAdd = af.AddFriends(self.logger, self.friendsTitles, self.tableHeaders)         #  Needs to be self. - to keep window alive.
            self.friendsAdd.show()
            self.friendsAdd.addNewFriend.connect(self.addNewFriend)                                     #  Signal is fired when a friend is to be added.
            self.friendsAdd.closeNewFriend.connect(self.closeNewFriend)                                 #  Signal is fired when the addFriend window is closed.
    # ----------------------------------------------------------------------------------------------------------------------- addNewFriend() --------
    def addNewFriend(self, friend):
        """  Adds a new Friend to the friends store.
             The friends store is then re-loaded, this ensures the data is sorted.
             LoadTable is called to refresh the displayed data.
        """
        key  = f"{friend[1]} : {friend[2]}"
        item = friend
        self.friendsStore.addFriend(key, item)
        self.refreshFriends()
    # ----------------------------------------------------------------------------------------------------------------------- editFriend() ----------
    def editFriend(self):
        row = self.tableView.currentRow()

        if row == -1:
            QMessageBox.information(self, "Error.", "No row selected.")
            return

        key    = f"{self.tableView.item(row, 1).text()} : {self.tableView.item(row, 2).text()}"
        friend = self.friendsStore.getFriend(key)
        self.friendsAdd = af.AddFriends(self.logger, self.friendsTitles, self.tableHeaders, friend)         #  Needs to be self. - to keep window alive.
        self.friendsAdd.show()
        self.friendsAdd.addNewFriend.connect(self.addNewFriend)                                             #  Signal is fired when a friend is to be added.
        self.friendsAdd.closeNewFriend.connect(self.closeNewFriend)   
    # ----------------------------------------------------------------------------------------------------------------------- deleteFriend() --------
    def deleteFriend(self):
        """  Deletes an event from the table.
             Displays an error if no row selected.
             Prompts user for confirmation.
        """
        row = self.tableView.currentRow()

        if row == -1:
            confirmation = QMessageBox.information(self, "Error.", "No row selected.")
            return

        name         = f"{self.tableView.item(row, 2).text()} {self.tableView.item(row, 1).text()}"
        confirmation = QMessageBox.question(self, "Confirmation", f"Delete a friend {name}")

        if confirmation == QMessageBox.StandardButton.Yes:
            key = f"{self.tableView.item(row, 1).text()} : {self.tableView.item(row, 2).text()}"
            self.friendsStore.deleteFriend(key)             #  Delete friend
            self.refreshFriends()
    # ----------------------------------------------------------------------------------------------------------------------- refreshFriends() ------
    def refreshFriends(self):
        """  Save the table to the friends store, the friends store is then re-loaded into the table.
             Called when a friend has been added, deleted or edited.
        """
        self.friendsStore.saveFriends()
        self.friends = self.friendsStore.getFriends()
        self.loadTable()
    # ----------------------------------------------------------------------------------------------------------------------- closeNewFriend() ------
    def closeNewFriend(self):
        """  When the newFriends window is closed, it signals here so the reference can be set to null.
        """
        self.friendsAdd = None
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        """  When the viewer is closed, checks if any child windows are still open.
        """
        if self.friendsAdd:
            confirmation = QMessageBox.question(self, "Confirmation", "The Add Friend's Windows is still open - Continue?")

            if confirmation == QMessageBox.StandardButton.Yes:
                event.accept()      #  Close the app.
                self.friendsAdd.close()
            else:
                event.ignore()      #  Continue the app.

