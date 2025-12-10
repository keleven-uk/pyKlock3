###############################################################################################################
#    pyKlock3   Copyright (C) <2025>  <Kevin Scott>                                                           #
#    A klock built using QT framework.                              .                                         #
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

from PyQt6.QtWidgets import (QMainWindow, QFrame, QToolBar, QLabel, QLCDNumber, QStackedLayout,QColorDialog,
                             QMessageBox, QFontDialog, QComboBox)
from PyQt6.QtGui     import QAction, QColor, QIcon, QFont
from PyQt6.QtCore    import Qt, QTimer, QDateTime, QSize, QPoint

import src.selectTime as st
import src.utils.klock_utils as utils                                 #  Need to install pywin32

from src.projectPaths import RESOURCE_PATH

class KlockWindow(QMainWindow):
    def __init__(self, myConfig, myLogger):
        super().__init__()

        self.config     = myConfig
        self.logger     = myLogger
        self.selectTime = st.SelectTime()
        self.timeFont   = QFont()

        self.setWindowTitle("pyKlock")
        self.setGeometry(self.config.X_POS, self.config.Y_POS, self.config.WIDTH, self.config.HEIGHT)
        self.setFixedSize(self.config.WIDTH, self.config.HEIGHT)

        self.foregroundColour = self.config.FOREGROUND
        self.backgroundColour = self.config.BACKGROUND
        self.timeMode         = self.config.TIME_MODE       #  Either Digital ot Text time.
        self.timeFormat       = self.config.TIME_FORMAT     #  The format of time to be displayed.
        self.transparent      = self.config.TRANSPARENT

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        if self.transparent:
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        #  result is the Boolean result of the conversion, True = success and False = error.
        result = QFont.fromString(self.timeFont, self.config.TIME_FONT)

        if not result:
            self.logger.error(f"Error converting the Time Font {result}")

        #  Build GUI
        self.buildGUI()
        self.buildStatusBar()
        self.buildComboBox()
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
        self.logger.info("Building GUI")
        #  Create a layout
        self.stackedLayout = QStackedLayout()

        #  Create an lcd Number display.
        self.lcdTime = QLCDNumber()
        self.lcdTime.setDigitCount(8)                                 # Display 8 digits
        self.lcdTime.display("12:34:56")                              # Show some initial value
        self.lcdTime.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)  # Use filled segment style

        #  Create the time text display.
        self.txtTime = QLabel("00:00:00")
        self.txtTime.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.txtTime.setFont(self.timeFont)

        # Add pages to the stacked layout.
        self.stackedLayout.addWidget(self.lcdTime)                    #  Index 0
        self.stackedLayout.addWidget(self.txtTime)                    #  Index 1

        #  Create a central widget.
        self.centralWidget = QFrame()
        self.centralWidget.setStyleSheet("margin:0px; border:0px")
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.stackedLayout)


        #  Set up timer to update the clock
        timer = QTimer(self)
        timer.timeout.connect(self.updateTime)
        timer.start(1000)

    def buildStatusBar(self):
        self.logger.info("Building Statusbar")
        """  Create a status bar
        """
        self.statusBar = self.statusBar()
        self.statusBar.setSizeGripEnabled(False)

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

    def buildComboBox(self):
        self.logger.info("Building Combobox")
        self.combo = QComboBox()
        self.combo.insertItems(1,self.selectTime.timeTypes)
        index = self.combo.findText(self.timeFormat)
        if index >= 0:
            self.combo.setCurrentIndex(index)

        self.combo.setStyleSheet("QComboBox"
                                 "{"
                                 "color        : self.foregroundColour;"
                                 "background   : transparent;"
                                 "border-radius: 3px;"
                                 "}")

    def buildMenu(self):
        """  Initialise the menu and add the actions.
        """
        self.logger.info("Building Menu")

        #  Set up actions.
        path = f"{RESOURCE_PATH}/digital-clock.png"
        self.actDigitalTime = QAction(QIcon(path),"Digital Time", self)
        self.actDigitalTime.triggered.connect(self.setDigitalTime)

        path = f"{RESOURCE_PATH}/time-text.png"
        self.actTextTime = QAction(QIcon(path),"Time in words", self)
        self.actTextTime.triggered.connect(self.setTextTime)
        self.actTextTime.setCheckable(False)

        path = f"{RESOURCE_PATH}/font.png"
        self.actFont = QAction(QIcon(path),"Change Font", self)
        self.actFont.triggered.connect(self.openFontDialog)
        self.actFont.setCheckable(False)

        path = f"{RESOURCE_PATH}/colour-swatch.png"
        self.actBackColour = QAction(QIcon(path),"Change Background Colour", self)
        self.actBackColour.triggered.connect(self.getBackColour)
        self.actBackColour.setCheckable(False)
        flag = False if self.transparent else True
        self.actBackColour.setEnabled(flag)

        path = f"{RESOURCE_PATH}/colour.png"
        self.actForeColour = QAction(QIcon(path),"Change Foreground Colour", self)
        self.actForeColour.triggered.connect(self.getForeColour)
        self.actForeColour.setCheckable(False)

        path = f"{RESOURCE_PATH}/cross.png"
        self.actClose = QAction(QIcon(path),"Close", self)
        self.actClose.triggered.connect(self.closeEvent)
        self.actClose.setCheckable(False)

        # Set up main menu
        self.menu = self.menuBar()

        mnuFile    = self.menu.addMenu("&File")
        mnuTime    = self.menu.addMenu("&Time")
        mnuDisplay = self.menu.addMenu("&Display")

        #  Set up menu actions.
        mnuFile.addAction(self.actClose)

        mnuDisplay.addAction(self.actBackColour)
        mnuDisplay.addAction(self.actForeColour)
        mnuDisplay.addSeparator()
        mnuDisplay.addAction(self.actFont)

        mnuTime.addAction(self.actDigitalTime)
        mnuTime.addAction(self.actTextTime)
        mnuTime.addSeparator()

        #  Set up toolbar.
        self.toolbar = QToolBar("Time Toolbar")
        self.toolbar.setIconSize(QSize(16, 16))
        self.toolbar.toggleViewAction().setEnabled(False)               #  to prevent this toolbar being removed.
        self.addToolBar(self.toolbar)

        #  Set up tool bar actions.
        self.toolbar.addAction(self.actDigitalTime)
        self.toolbar.addAction(self.actTextTime)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.combo)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actFont)
        self.toolbar.addAction(self.actBackColour)
        self.toolbar.addAction(self.actForeColour)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actClose)

    #  -------------------------------------------------------------------------------------------------------------------- openFontDialog ----------
    def openFontDialog(self):
        font, ok = QFontDialog.getFont(self.txtTime.font(), self, "Choose Fomt for Time.")

        # If user clicked OK, update the label's font
        if ok:
            self.txtTime.setFont(font)
            self.timeFont = font
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
            self.timeFormat = self.combo.currentText()
            self.txtTime.setText(self.selectTime.getTime(self.timeFormat))
            self.stsFrmt.setText(f"{self.timeFormat}")

        self.stsDate.setText(txtDate)
        self.stsState.setText(f"{utils.getState()}")
        self.stsIdle.setText(utils.getIdleDuration())
    # ----------------------------------------------------------------------------------------------------------------------- updateColour() --------
    def updateColour(self):
        """  Update the foreground and background colour of both the main form and the statusbar.
             Set the config values and re-write the config file.
        """
        #  Just in case it is called in TRANSPARENT mode - spoils the display.
        #  So, just update the foreground colour of the timer and statusbar.
        if self.transparent:
            self.txtTime.setStyleSheet(f"color: {self.foregroundColour}")
            self.statusBar.setStyleSheet(f"color: {self.foregroundColour}")
            self.menu.setStyleSheet(f"color: {self.foregroundColour}")
            self.toolbar.setStyleSheet(f"color: {self.foregroundColour}")
            return

        self.centralWidget.setStyleSheet(f"color: {self.foregroundColour}; background-color: {self.backgroundColour}; margin:0px; border:0px")
        self.statusBar.setStyleSheet(f"color: {self.foregroundColour}; background-color: {self.backgroundColour}")
        self.menu.setStyleSheet(f"color: {self.foregroundColour}; background-color: {self.backgroundColour}")
        self.toolbar.setStyleSheet(f"color: {self.foregroundColour}; background-color: {self.backgroundColour}")
    # ----------------------------------------------------------------------------------------------------------------------- setDigitalTime() ------
    def setDigitalTime(self):
        """  Bring forward the digital time display, hides the text time display.
        """
        self.stackedLayout.setCurrentIndex(0)
        # self.actDigitalTime.setCheckable(True)
        # self.actTextTime.setCheckable(False)
        # self.mnuTimeFormatTime.setEnabled(False)
        self.timeMode = "Digital"
    # ----------------------------------------------------------------------------------------------------------------------- setWordTime() ---------
    def setTextTime(self):
        """  Bring forward the text time display, hides the digital time display.
        """
        self.stackedLayout.setCurrentIndex(1)
        # self.actDigitalTime.setCheckable(False)
        # self.actTextTime.setCheckable(True)
        # self.mnuTimeFormatTime.setEnabled(True)
        self.timeMode = "Text"
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
    # ----------------------------------------------------------------------------------------------------------------------- mousePressEvent -------
    #  The three following methods are in place of the default mouse events - so pyKlocvk can be dragged
    #  by holding the left mouse button [anywhere in pyKlock] and moving the mouse.
    #  Stole from - https://stackoverflow.com/questions/37718329/pyqt5-draggable-frameless-window
    def mousePressEvent(self, event):
        self.oldPos = event.position().toPoint()
    # ----------------------------------------------------------------------------------------------------------------------- mouseMoveEvent --------
    def mouseMoveEvent(self, event):
        delta = QPoint(event.position().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
    # ----------------------------------------------------------------------------------------------------------------------- mouseReleaseEvent -----
    def mouseReleaseEvent(self, event):
        self.oldPos = event.position().toPoint()
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        """  Ask for confirmation before closing, if required.

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
            self.close()        # Close the app
    # ----------------------------------------------------------------------------------------------------------------------- saveConfig() ----------
    def saveConfig(self):
        """  Save stuff to the config file, in case any has changed.
        """
        self.config.X_POS       = self.x()
        self.config.Y_POS       = self.y()
        self.config.WIDTH       = self.width()
        self.config.HEIGHT      = self.height()
        self.config.TIME_MODE   = self.timeMode
        self.config.TIME_FONT   = self.timeFont.toString()
        self.config.TIME_FORMAT = self.timeFormat
        self.config.TRANSPARENT = self.transparent
        self.config.FOREGROUND  = self.foregroundColour
        self.config.BACKGROUND  = self.backgroundColour
        self.config.writeConfig()
