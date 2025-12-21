###############################################################################################################
#    Settings   Copyright (C) <2025>  <Kevin Scott>                                                           #
#                                                                                                             #
#    Displays an settings dialog.                                                                             #
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

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QDialogButtonBox, QTabWidget, QWidget, QFormLayout,
                             QApplication)


class Page(QWidget):
    def __init__(self):
        super().__init__()

        page_layout = QFormLayout()
        self.setLayout(page_layout)

class Settings(QDialog):
    def __init__(self, parent, myConfig, myLogger):
        super().__init__(parent)

        self.config = myConfig
        self.logger = myLogger
        self.height = 600
        self.width  = 400
        screenSize  = QApplication.primaryScreen().availableGeometry()
        xPos        = int((screenSize.width() / 2)  - (self.width / 2))
        yPos        = int((screenSize.height() / 2) - (self.height / 2))

        self.logger.info("Launching Settings dialog")

        self.setWindowTitle(f"PyKlock Settings {self.config.NAME}")
        self.setGeometry(xPos, yPos, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        layout = QVBoxLayout()

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.clicked.connect(self.buttonClicked)

        twTab = QTabWidget()

        tabs  = ["Info", "Application", "Display", "Time"]
        funcs = [self.Info, self.Application, self.Display, self.Time]

        for pos, tab in enumerate(tabs):
            page = Page()
            twTab.addTab(page, tab)
            funcs[pos]()

        layout.addWidget(twTab)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def Info(self):
        print("Info")

    def Application(self):
        print("Application")

    def Display(self):
        print("Display")

    def Time(self):
        print("Time")

    def buttonClicked(self, button):
        role = self.buttonBox.standardButton(button)
        if role == QDialogButtonBox.StandardButton.Cancel:
            self.close()
        elif role == QDialogButtonBox.StandardButton.Ok:
            self.config.writeConfig()
            self.close()

    def closeEvent(self, event):
        self.logger.info("Settings Close Event")
        event.accept()


