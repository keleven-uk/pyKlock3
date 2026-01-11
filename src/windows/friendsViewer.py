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

from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QMainWindow, QFrame, QTableWidget, QTableWidgetItem,
                             QTableWidget)

import src.classes.friendsStore as fs


class FriendsViewer(QMainWindow):
    """  Display friends in a table in a separate window.
    """
    def __init__(self, myLogger):
        super().__init__()

        self.logger       = myLogger
        self.friendsStore = fs.friendsStore(self.logger)
        self.tableHeaders = self.friendsStore.getHeaders
        self.noHeaders    = len(self.tableHeaders)

        self.setGeometry(300, 300, 1500, 800)
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

        self.tableView = QTableWidget()
        self.tableView.setColumnCount(self.noHeaders)
        self.tableView.setHorizontalHeaderLabels(self.tableHeaders)

        btnClose = QPushButton(text="Close", parent=self)
        btnClose.clicked.connect(self.close)

        self.centralLayout.addWidget(self.tableView)
        self.centralLayout.addWidget(btnClose)

        self.centralWidget.setLayout(self.centralLayout)

    def loadTable(self):
        """
        """
        row     = 0
        friends = self.friendsStore.getFriends()

        for friend in friends:
            self.tableView.insertRow(row)
            col = 0
            for item in friend:
                self.tableView.setItem(row, col, QTableWidgetItem(item))
                col += 1

            row += 1


    def closeEvent(self, event):
        pass
