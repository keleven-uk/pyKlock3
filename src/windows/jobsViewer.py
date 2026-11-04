###############################################################################################################
#    jobsViewer   Copyright (C) <2026>  <Kevin Scott>                                                         #
#                                                                                                             #
#    Display jobs in a table.                                                                                 #
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

import src.windows.eventsAdd as ae

class JobsViewer(QMainWindow):
    """  Display friends in a table in a separate window.
    """
    def __init__(self, myLogger, myConfig, jobsStore):
        super().__init__()

        self.logger           = myLogger
        self.config           = myConfig
        self.jobsStore        = jobsStore
        self.jobs             = self.jobsStore.getJobs()
        self.eventsCategories = self.jobsStore.getCategories
        self.tableHeaders     = self.jobsStore.getHeaders
        self.noHeaders        = len(self.tableHeaders)
        self.eventsAdd        = None

        self.height      = 600
        self.width       = 200
        self.screenSize  = QApplication.primaryScreen().availableGeometry()
        self.xPos        = int((self.screenSize.width() / 2)  - (self.width / 2))
        self.yPos        = int((self.screenSize.height() / 2) - (self.height / 2))

        self.setGeometry(self.xPos, self.yPos, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("Jobs")

        self.buildGUI()
        self.loadTable()

    def buildGUI(self):
        """  Build the GUI elements.
        """
        #  Create a central widget.
        self.centralWidget = QFrame()
        self.setCentralWidget(self.centralWidget)
        self.centralLayout = QVBoxLayout()
        self.ButtonLayout  = QHBoxLayout()

        self.tableView = QTableWidget()
        self.tableView.setColumnCount(self.noHeaders)
        self.tableView.setHorizontalHeaderLabels(self.tableHeaders)

        btnAdd = QPushButton(text="Add an Event", parent=self)
        #btnAdd.clicked.connect(self.addEvent)

        btnEdit = QPushButton(text="Edit an Event", parent=self)
        #btnEdit.clicked.connect(self.editEvent)

        btnDelete = QPushButton(text="Delete an Event", parent=self)
        #btnDelete.clicked.connect(self.deleteEvent)

        btnRefresh = QPushButton(text="Refresh Events", parent=self)
        #btnRefresh.clicked.connect(self.refreshEvents)

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
    def loadTable(self, refresh=False):
        """  Populate the table with jobs data.
             The finds data is a list of lists.

             If table being drawn for the first time, either after an add or initially - Do not add width offset.
        """
        row = 0

        self.tableView.clear()
        self.tableView.setRowCount(row)
        self.tableView.setColumnCount(self.noHeaders)
        self.tableView.setHorizontalHeaderLabels(self.tableHeaders)

        for job in self.jobs:
            self.tableView.insertRow(row)
            col = 0
            for item in job:
                self.tableView.setItem(row, col, QTableWidgetItem(item))
                col += 1

            row += 1

        for head in range(self.noHeaders):
            self.tableView.resizeColumnToContents(head)

        if not refresh:
            self.width = self.tableView.width() + 120
            
        self.xPos = int((self.screenSize.width() / 2)  - (self.width / 2))
        self.yPos = int((self.screenSize.height() / 2) - (self.height / 2))
        self.setGeometry(self.xPos, self.yPos, self.width, self.height)
        self.setFixedSize(self.width, self.height)



 
