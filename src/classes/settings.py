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
                             QApplication, QLineEdit, QPushButton, QColorDialog, QComboBox, QFontDialog)
from PyQt6.QtGui     import QIcon, QColor, QFont

from src.projectPaths import RESOURCE_PATH

import src.selectTime as st


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
        self.height = 400
        self.width  = 400
        screenSize  = QApplication.primaryScreen().availableGeometry()
        xPos        = int((screenSize.width() / 2)  - (self.width / 2))
        yPos        = int((screenSize.height() / 2) - (self.height / 2))

        self.logger.info("Launching Settings dialog")

        self.setWindowTitle(f"PyKlock Settings {self.config.NAME}")
        self.setGeometry(xPos, yPos, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        self.selectTime       = st.SelectTime()
        self.timeFont         = QFont()
        self.foregroundColour = self.config.FOREGROUND
        self.backgroundColour = self.config.BACKGROUND
        self.update           = False

        layout = QVBoxLayout()

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.clicked.connect(self.buttonClicked)

        self.twTab = QTabWidget()

        funcs = [self.Info, self.Application, self.Display, self.Time]

        for func in funcs:
            func()

        layout.addWidget(self.twTab)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
    # ----------------------------------------------------------------------------------------------------------------------- Info() ----------------
    def Info(self):
        """  Display application Info.
             Both name and Version are for display only.
        """
        page   = QWidget(self.twTab)
        layout = QFormLayout()
        page.setLayout(layout)

        lbName = QLineEdit(self.config.NAME, self)
        lbName.setReadOnly(True)
        lbVersion = QLineEdit(self.config.VERSION, self)
        lbVersion.setReadOnly(True)

        layout.addRow("Name ", lbName)                                 #  Name is read only.
        layout.addRow("Version ", lbVersion)                           #  Version is read only.

        self.twTab.addTab(page, "Application Info")
    # ----------------------------------------------------------------------------------------------------------------------- Application() ---------
    def Application(self):
        """  Display application data.
             Can be used to reset screen position.
             Width and height are calculated by the app, so might be ignored.

             NB : application x, y, width & hight - are stored as int, but display as strings.
        """
        page = QWidget(self.twTab)
        layout = QFormLayout()
        page.setLayout(layout)

        # create a push button.
        path = f"{RESOURCE_PATH}/cross.png"
        self.btnConfirmExit = QPushButton()
        self.btnConfirmExit.setIcon(QIcon(path))
        self.btnConfirmExit.setCheckable(True)
        checked = True if self.config.CONFIRM_EXIT else False
        self.btnConfirmExit.setDefault(checked)
        self.btnConfirmExit.clicked.connect(self.toggleConfirmExit)

        layout.addRow("X Position - Main Window ", QLineEdit(str(self.config.X_POS),  self))
        layout.addRow("Y Position - Main Window ", QLineEdit(str(self.config.Y_POS),  self))
        layout.addRow("Width - Main Window ", QLineEdit(str(self.config.WIDTH),  self))
        layout.addRow("Height - Main Window ", QLineEdit(str(self.config.HEIGHT), self))
        layout.addRow("Confirm Exit ", self.btnConfirmExit)

        self.twTab.addTab(page, "Application Data")

    def toggleConfirmExit(self, checked):
        """  Toggles the checked state of the Confirm Exit button.
        """
        checked = not checked
        self.btnConfirmExit.setDefault(checked)
    # ----------------------------------------------------------------------------------------------------------------------- Display() -------------
    def Display(self):
        page = QWidget(self.twTab)
        layout = QFormLayout()
        page.setLayout(layout)

        # create a button.
        path = f"{RESOURCE_PATH}/colour.png"
        self.btnForeColour = QPushButton()
        self.btnForeColour.setIcon(QIcon(path))
        self.btnForeColour.setStyleSheet(f"color: {self.foregroundColour}")
        self.btnForeColour.clicked.connect(self.getForeColour)
        path = f"{RESOURCE_PATH}/colour-swatch.png"
        self.btnBackColour = QPushButton()
        self.btnBackColour.setIcon(QIcon(path))
        self.btnBackColour.setStyleSheet(f"background-color: {self.backgroundColour}")
        self.btnBackColour.clicked.connect(self.getBackColour)

        leTransparent = QLineEdit("Amend in config.toml and restart", self)
        leTransparent.setReadOnly(True)
        btnInfoLine = QPushButton()
        btnInfoLine.setCheckable(True)
        checked = True if self.config.INFO_LINE else False
        btnInfoLine.setDefault(checked)

        layout.addRow("Foreground Colour ", self.btnForeColour)
        layout.addRow("Background Colour ", self.btnBackColour)
        layout.addRow("Transparent Background ", leTransparent)
        layout.addRow("Information Line ", btnInfoLine)

        self.twTab.addTab(page, "Display")

    def getForeColour(self):
        """  launch the colour input dialog and obtain the new foreground colour.
        """
        self.current_color = QColor(self.foregroundColour)
        colour = QColorDialog.getColor(self.current_color, self, "Choose Foreground Colour")
        if colour.isValid():
            self.foregroundColour = colour.name()

    def getBackColour(self):
        """  launch the colour input dialog and obtain the new background colour.
        """
        self.current_color = QColor(self.backgroundColour)
        colour = QColorDialog.getColor(self.current_color, self, "Choose Background Colour")
        if colour.isValid():
            self.backgroundColour = colour.name()
    # ----------------------------------------------------------------------------------------------------------------------- Time() ----------------
    def Time(self):
        page = QWidget(self.twTab)
        layout = QFormLayout()
        page.setLayout(layout)

        self.cbTimeMode = QComboBox()
        self.cbTimeMode.insertItems(1, ["Digital", "Text"])
        self.cbTimeFmt = QComboBox()
        self.cbTimeFmt.insertItems(1, self.selectTime.timeTypes)
        self.cbTimeAllign = QComboBox()
        self.cbTimeAllign.insertItems(1, ["Left", "Right", "None"])
        # create a button.
        path = f"{RESOURCE_PATH}/font.png"
        self.btnFont = QPushButton()
        self.btnFont.setIcon(QIcon(path))
        self.btnFont.clicked.connect(self.openFontDialog)

        layout.addRow("Foreground Colour ", self.cbTimeMode)
        layout.addRow("Foreground Colour ", self.cbTimeFmt)
        layout.addRow("Time Font ", self.btnFont)
        layout.addRow("Foreground Colour ", self.cbTimeAllign)
        layout.addRow("prefix Character ", QLineEdit(str(self.config.TIME_PREFIX), self))
        layout.addRow("postfix Character ", QLineEdit(str(self.config.TIME_POSTFIX), self))
        layout.addRow("space Character ", QLineEdit(str(self.config.TIME_SPACE), self))

        self.twTab.addTab(page, "Time")

    def openFontDialog(self):
        """  Open the font dialog.
        """
        font, ok = QFontDialog.getFont(self.timeFont, self, "Choose Font for Time.")

        # If user clicked OK, update the label's font
        if ok:
            self.timeFont = font
    # ----------------------------------------------------------------------------------------------------------------------- buttonClicked() -------
    def buttonClicked(self, button):
        role = self.buttonBox.standardButton(button)
        if role == QDialogButtonBox.StandardButton.Cancel:
            self.close()
        elif role == QDialogButtonBox.StandardButton.Ok:
            self.config.writeConfig()
            self.close()
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        self.logger.info("Settings Close Event")
        event.accept()


