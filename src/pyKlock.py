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

import pathlib
import functools

from PyQt6.QtWidgets import (QMainWindow, QFrame, QToolBar, QLabel, QLCDNumber, QStackedLayout,
                             QColorDialog, QMessageBox, QFontDialog)
from PyQt6.QtGui     import QAction, QColor, QIcon, QFont
from PyQt6.QtCore    import Qt, QTimer, QDateTime, QSize

import src.selectTime as st
import src.utils.klock_utils as utils                                 #  Need to install pywin32

from src.projectPaths import RESOURCE_PATH

class KlockWindow(QMainWindow):
    def __init__(self, myConfig):
        super().__init__()

        self.config     = myConfig
        self.selectTime = st.SelectTime()
        self.timeFont   = QFont()

        self.setWindowTitle("pyKlock")
        self.setGeometry(self.config.X_POS, self.config.Y_POS, self.config.WIDTH, self.config.HEIGHT)

        self.foregroundColour = self.config.FOREGROUND
        self.backgroundColour = self.config.BACKGROUND
        self.timeMode         = self.config.TIME_MODE
        self.timeFormat       = self.config.TIME_FORMAT
        #  dummy is the Boolean result of the conversion, True = success and False = error.
        dummy                 = QFont.fromString(self.timeFont, self.config.TIME_FONT)

        #  Build GUI
        self.buildGUI()
        self.buildStatusbar()
        self.buildMenu()

        #  Initialize state
        if self.config.TIME_MODE == "Digital":
            self.setDigitalTime()
        else:
            self.setTextTime()

        self.updateColour()
        self.updateTime()

    def buildGUI(self):
        """  Set up the GUI widgets.
        """
        #  Create a layout
        self.stackedLayout = QStackedLayout()

        #  Create an lcd Number display
        self.lcdTime = QLCDNumber()
        self.lcdTime.setDigitCount(8)                                 # Display 8 digits
        self.lcdTime.display("12:34:56")                              # Show some initial value
        self.lcdTime.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)  # Use filled segment style

        self.txtTime = QLabel("00:00:00")
        self.txtTime.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.txtTime.setFont(self.timeFont)

        # Add pages to the stacked layout
        self.stackedLayout.addWidget(self.lcdTime)                    #  Index 0
        self.stackedLayout.addWidget(self.txtTime)                    #  Index 1

        #  Create a central widget
        self.centralWidget = QFrame()
        self.centralWidget.setStyleSheet("margin:0px; border:0px")
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.stackedLayout)


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
        self.stsFrmt  = QLabel("L.E.D.")
        self.stsIdle  = QLabel("idle : 7s")

        self.stsDate.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.stsState.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stsFrmt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stsIdle.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.statusBar.addPermanentWidget(self.stsDate,  1)
        self.statusBar.addPermanentWidget(self.stsState, 1)
        self.statusBar.addPermanentWidget(self.stsFrmt, 1)
        self.statusBar.addPermanentWidget(self.stsIdle,  2)

    def buildMenu(self):
        """  Initialise the menu and add the actions.
        """
        #  Set up actions.
        actExit = QAction("Exit", self)
        actExit.triggered.connect(self.close)

        actForeColour = QAction("Foreground Colour", self)
        actForeColour.triggered.connect(self.getForeColour)

        actBackColour = QAction("Background Colour", self)
        actBackColour.triggered.connect(self.getBackColour)

        path = f"{RESOURCE_PATH}/digital-clock.png"
        self.actDigitalTime = QAction(QIcon(path),"Digital Time", self)
        self.actDigitalTime.triggered.connect(self.setDigitalTime)
        self.actDigitalTime.setCheckable(True)

        path = f"{RESOURCE_PATH}/time-text.png"
        self.actTextTime = QAction(QIcon(path),"Time in words", self)
        self.actTextTime.triggered.connect(self.setTextTime)
        self.actTextTime.setCheckable(False)

        self.actTimeFormat = QAction("Time Font", self)
        self.actTimeFormat.triggered.connect(self.openFontDialog)
        # Set up main menu
        self.menu = self.menuBar()

        mnuFile    = self.menu.addMenu("&File")
        mnuTime    = self.menu.addMenu("&Time")
        mnuDisplay = self.menu.addMenu("&Display")

        #  Set up menu actions.
        mnuFile.addAction(actExit)
        mnuDisplay.addAction(actForeColour)
        mnuDisplay.addAction(actBackColour)
        mnuTime.addAction(self.actDigitalTime)
        mnuTime.addAction(self.actTextTime)
        mnuTime.addSeparator()

        self.mnuTimeFormatTime = mnuTime.addMenu("Format")
        for item in self.selectTime.timeTypes:
            self.mnuTimeFormatTime.addAction(item, functools.partial(self.changeTimeFormat, item))

        mnuTime.addSeparator()
        mnuTime.addAction(self.actTimeFormat)


        #  Set up toolbar.
        self.toolbar = QToolBar("Time Toolbar")
        self.toolbar.setIconSize(QSize(16, 16))
        self.toolbar.toggleViewAction().setEnabled(False)               #  to prevent this toolbar being removed.
        self.addToolBar(self.toolbar)

        #  Set up tool bar actions.
        self.toolbar.addAction(self.actDigitalTime)
        self.toolbar.addAction(self.actTextTime)

    # ----------------------------------------------------------------------------------------------------------------------- openFontDialog ------
    def openFontDialog(self):
        font, ok = QFontDialog.getFont(self.txtTime.font(), self, "Choose Fomt for Time.")

        # If user clicked OK, update the label's font
        if ok:
            self.txtTime.setFont(font)
            self.timeFont = font
    # ----------------------------------------------------------------------------------------------------------------------- changeTimeFormat ------
    def changeTimeFormat(self, value):
        """  Changes the format of the text time.
             The value is received from the Format sub-menu under main menu Time
        """
        self.timeFormat = value
        self.sender().setCheckable(True)
    # ----------------------------------------------------------------------------------------------------------------------- setDigitalTime() ------
    def setDigitalTime(self):
        """  Bring forward the digital time display, hides the text time display.
        """
        self.stackedLayout.setCurrentIndex(0)
        self.actDigitalTime.setCheckable(True)
        self.actTextTime.setCheckable(False)
        self.mnuTimeFormatTime.setEnabled(False)
        self.timeMode = "Digital"
    # ----------------------------------------------------------------------------------------------------------------------- setWordTime() ---------
    def setTextTime(self):
        """  Bring forward the text time display, hides the digital time display.
        """
        self.stackedLayout.setCurrentIndex(1)
        self.actDigitalTime.setCheckable(False)
        self.actTextTime.setCheckable(True)
        self.mnuTimeFormatTime.setEnabled(True)
        self.timeMode = "Text"
    # ----------------------------------------------------------------------------------------------------------------------- updateTime() ----------
    def updateTime(self):
        """  Update the time and status bar.            self.selectTime.getTime(self.myConfig.TIME_TYPE)
        """
        dtCentral = QDateTime.currentDateTime()
        txtTime   = dtCentral.toString("hh:mm:ss")
        txtDate   = dtCentral.toString("dddd MMMM yyyy")

        if self.timeMode == "Digital":
            self.lcdTime.display(txtTime)
            self.stsFrmt.setText("L.E.D.")
        else:
            self.txtTime.setText(self.selectTime.getTime(self.timeFormat))
            self.stsFrmt.setText(f"{self.timeFormat}")

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
        self.toolbar.setStyleSheet(f"color: {self.foregroundColour}; background-color: {self.backgroundColour}")

        self.config.FOREGROUND = self.foregroundColour
        self.config.BACKGROUND = self.backgroundColour
        self.config.writeConfig()
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        """  Ask for confirmation before closing

             Save new config properties to file.
        """
        if self.config.CONFIRM_EXIT:
            confirmation = QMessageBox.question(self, "Confirmation", "Are you sure you want to close the application?")

            if confirmation == QMessageBox.StandardButton.Yes:
                self.saveConfig()
                event.accept()  # Close the app
            else:
                event.ignore()  # Don't close the app
        else:
            self.saveConfig()
    # ----------------------------------------------------------------------------------------------------------------------- saveConfig() ----------
    def saveConfig(self):
        self.config.X_POS     = self.x()
        self.config.Y_POS     = self.y() + 31     #  This seems to move 32 upwards on closing - need to investigate.
        self.config.WIDTH     = self.width()
        self.config.HEIGHT    = self.height()
        self.config.TIME_MODE = self.timeMode
        self.config.TIME_FONT = self.timeFont.toString()
        self.config.writeConfig()












