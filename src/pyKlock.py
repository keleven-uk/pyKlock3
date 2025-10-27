###############################################################################################################
#    pyKlock3   Copyright (C) <2025>  <Kevin Scott>                                                           #                                                                                                             #    A klock built using QT framework.                              .                                         #
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

from PyQt6.QtWidgets import (QMainWindow, QFrame, QLabel, QLCDNumber, QVBoxLayout, QColorDialog, QMessageBox)
from PyQt6.QtGui     import QAction, QColor
from PyQt6.QtCore    import Qt, QTimer, QDateTime

import src.utils.klock_utils as utils                                 #  Need to install pywin32


class KlockWindow(QMainWindow):
    def __init__(self, myConfig):
        super().__init__()

        self.config = myConfig
        self.setWindowTitle("pyKlock")
        self.setGeometry(self.config.X_POS, self.config.Y_POS, self.config.WIDTH, self.config.HEIGHT)

        self.foregroundColour = self.config.FOREGROUND
        self.backgroundColour = self.config.BACKGROUND

        #  Build GUI
        self.buildGUI()
        self.buildStatusbar()
        self.buildMenu()

        #  Initialize state
        self.updateColour()
        self.updateTime()

    def buildGUI(self):
        """  Set up the GUI widgets.
        """
        #  Create a central widget
        self.centralWidget = QFrame()
        self.centralWidget.setStyleSheet("margin:0px; border:0px")
        self.setCentralWidget(self.centralWidget)

        #  Create a layout
        lytCentral = QVBoxLayout()
        self.centralWidget.setLayout(lytCentral)

        #  Create an lcd Number display
        self.lcdTime = QLCDNumber()
        self.lcdTime.setDigitCount(8)                                 # Display 8 digits
        self.lcdTime.display("12:34:56")                              # Show some initial value
        self.lcdTime.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)  # Use filled segment style

        # Add lcdTime to the layout
        lytCentral.addWidget(self.lcdTime)

        #  Set up timer to update the clock
        timer = QTimer(self)
        timer.timeout.connect(self.updateTime)
        timer.start(1000)                                             # Update every second

    def buildStatusbar(self):
        """  Create a status bar
        """
        self.statusBar = self.statusBar()

        self.stsDate  = QLabel("Thursday 23 October 2025")
        self.stsState = QLabel("cisN")
        self.stsIdle  = QLabel("idle : 7s")

        self.stsDate.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.stsState.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stsIdle.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.statusBar.addPermanentWidget(self.stsDate,  1)
        self.statusBar.addPermanentWidget(self.stsState, 1)
        self.statusBar.addPermanentWidget(self.stsIdle,  2)

    def buildMenu(self):
        """  Set up menu actions.
        """
        actExit = QAction("Exit", self)
        actExit.triggered.connect(self.close)

        actForeColour = QAction("Foreground Colour", self)
        actForeColour.triggered.connect(self.getForeColour)

        actBackColour = QAction("Background Colour", self)
        actBackColour.triggered.connect(self.getBackColour)

        # Set up main menu
        self.menu = self.menuBar()

        mnuFile    = self.menu.addMenu("&File")
        mnuDisplay = self.menu.addMenu("&Display")

        mnuFile.addAction(actExit)
        mnuDisplay.addAction(actForeColour)
        mnuDisplay.addAction(actBackColour)

    # ----------------------------------------------------------------------------------------------------------------------- updateTime() ----------
    def updateTime(self):
        """  Update the time and status bar.
        """
        dtCentral = QDateTime.currentDateTime()
        txtTime   = dtCentral.toString("hh:mm:ss")
        txtDate   = dtCentral.toString("dddd MMMM yyyy")

        self.lcdTime.display(txtTime)
        self.stsDate.setText(txtDate)
        self.stsState.setText(f"{utils.getState()}")
        self.stsIdle.setText(utils.getIdleDuration())
    # ----------------------------------------------------------------------------------------------------------------------- getForeColour() -------
    def getForeColour(self):
        """  launch the colour input dialog and obtain the new foreground colour.
        """
        self.current_color = QColor(self.foregroundColour)
        colour = QColorDialog.getColor(self.current_color, self, "Choose Foreground Colour")
        if colour.isValid():
            self.foregroundColour = colour.name()
            self.updateColour()
    # ----------------------------------------------------------------------------------------------------------------------- getBackColour() -------
    def getBackColour(self):
        """  launch the colour input dialog and obtain the new background colour.
        """
        self.current_color = QColor(self.backgroundColour)
        colour = QColorDialog.getColor(self.current_color, self, "Choose Background Colour")
        if colour.isValid():
            self.backgroundColour = colour.name()
            self.updateColour()
    # ----------------------------------------------------------------------------------------------------------------------- updateColour() --------
    def updateColour(self):
        """  Update the foreground and background colour of both the main form and the statusbar.
             Set the config values and re-write the config file.
        """
        self.centralWidget.setStyleSheet(f"color: {self.foregroundColour}; background-color: {self.backgroundColour}; margin:0px; border:0px")
        self.statusBar.setStyleSheet(f"color: {self.foregroundColour}; background-color: {self.backgroundColour}")
        self.menu.setStyleSheet(f"color: {self.foregroundColour}; background-color: {self.backgroundColour}")

        self.config.FOREGROUND = self.foregroundColour
        self.config.BACKGROUND = self.backgroundColour
        self.config.writeConfig()


    def closeEvent(self, event):
        # Ask for confirmation before closing
        confirmation = QMessageBox.question(self, "Confirmation", "Are you sure you want to close the application?")

        if confirmation == QMessageBox.StandardButton.Yes:
            event.accept()  # Close the app
            self.config.X_POS  = self.x()
            self.config.Y_POS  = self.y()
            self.config.WIDTH  = self.width()
            self.config.HEIGHT = self.height()
            self.updateColour()
        else:
            event.ignore()  # Don't close the app












