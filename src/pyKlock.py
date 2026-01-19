###############################################################################################################
#    pyKlock3   Copyright (C) <2025-26>  <Kevin Scott>                                                        #
#    A klock built using QT framework.                                                                        #
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

import time

from PyQt6.QtWidgets import (QMainWindow, QFrame, QLabel, QLCDNumber, QStackedLayout, QColorDialog,
                             QMessageBox, QFontDialog, QApplication, QHBoxLayout, QVBoxLayout,
                             QProgressBar)
from PyQt6.QtGui     import QColor, QFont
from PyQt6.QtCore    import Qt, QPoint, QTimer, QDateTime, pyqtSlot

import src.utils.klock_utils as utils                                 #  Need to install pywin32

import src.classes.menu as mu
import src.classes.sounds as snds
import src.classes.selectTime as st
import src.classes.systemInfo as si
import src.classes.progressBarStyles as styles

import src.windows.about as About
import src.windows.textViewer as tw
import src.windows.helpViewer as hp
import src.windows.settings as stngs


class KlockWindow(QMainWindow):
    def __init__(self, myConfig, myLogger):
        super().__init__()

        self.config = myConfig
        self.logger = myLogger

        self.updateValues()

        self.setWindowTitle("pyKlock")
        self.setGeometry(self.Xpos, self.Ypos, self.width, self.height)

        self.selectTime       = st.SelectTime()
        self.systemInfo       = si.SysInfo()
        self.pbStyles         = styles.Styles()             #  Styles for the battery progress bar.
        self.sounds           = snds.Sounds(self.config, self.logger)
        self.timeFont         = QFont()
        self.textWindow       = None                        #  No text external window yet.
        self.helpWindow       = None
        self.startTime        = time.perf_counter()
        self.lblWidth         = 0                           #  Used to measure size of time text and do we need to resize.
        self.lblHeight        = 0

        self.nowTotalBytesReceived  = self.systemInfo.TotalRawBytesReceived        #  Use to measure network speed.
        self.nowTotalBytesSent      = self.systemInfo.TotalRawBytesSent
        self.lastTotalBytesReceived = self.nowTotalBytesReceived
        self.lastTotalBytesSent     = self.nowTotalBytesSent
        self.newTime                = time.time()
        self.lastTime               = self.newTime

        self.menu   = mu.Menu(self.config, self.logger, self)
        self.myMenu = self.menu.buildMenu()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        if self.transparent:
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            self.setStyleSheet("background   : transparent;")

        #  result is the Boolean result of the conversion, True = success and False = error.
        result = QFont.fromString(self.timeFont, self.config.TIME_FONT)

        if not result:
            self.logger.error(f"Error converting the Time Font {result}")

        #  Build GUI
        self.buildGUI()
        self.buildStatusBar()
        self.menu.buildComboBox()
        self.setMenuBar(self.myMenu)
        self.addToolBar(self.menu.buildToolBar())
        self.menu.buildContextMenu()

        self.myMenu.setVisible(self.menu_bar)
        self.menu.toolbar.setVisible(self.tool_bar)

        #  Initialize state
        if self.config.TIME_MODE == "Digital":
            self.setDigitalTime()
        else:
            self.setTextTime()

        self.updateColour()
        self.updateTime()

    def updateValues(self):
        """  Set up run time values from the config file.
             Also called if the config file changes.
        """
        self.Xpos             = self.config.X_POS
        self.Ypos             = self.config.Y_POS
        self.width            = self.config.WIDTH
        self.height           = self.config.HEIGHT
        self.menu_bar         = self.config.MENU_BAR        #  menu and menuBar are already reserved by QT.
        self.tool_bar         = self.config.TOOL_BAR
        self.timeMode         = self.config.TIME_MODE       #  Either Digital ot Text time.
        self.timeFormat       = self.config.TIME_FORMAT     #  The format of time to be displayed.
        self.transparent      = self.config.TRANSPARENT
        self.foregroundColour = self.config.FOREGROUND
        self.backgroundColour = self.config.BACKGROUND

    def buildGUI(self):
        """  Set up the GUI widgets.
        """
        self.logger.info(" Building GUI.")
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
        self.centralLayout = QVBoxLayout()

        self.centralLayout.addLayout(self.stackedLayout)
        if self.config.INFO_LINE:
            self.buildInfoLine()

        self.centralWidget.setLayout(self.centralLayout)

        #  Set up timer to update the clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)

    def buildInfoLine(self):
        """  Create Info Line
        """
        self.logger.info(" Building Info Line.")
        self.stsCPU   = QLabel("CPU : 0%")
        self.stsRAM   = QLabel("RAM : 0%")
        self.stsDisc  = QLabel("C: [          ]")
        self.stsSpeed = QLabel("↓ 1.0 Mbit/s  ↑ 1.0 Mbit/s")

        self.infoLayout = QHBoxLayout()
        self.infoLayout.addWidget(self.stsCPU)
        self.infoLayout.addStretch()
        self.infoLayout.addWidget(self.stsRAM)
        self.infoLayout.addStretch()
        self.infoLayout.addWidget(self.stsDisc)
        self.infoLayout.addStretch()
        self.infoLayout.addWidget(self.stsSpeed)
        self.infoLayout.addStretch()

        self.stsCPU.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.stsRAM.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.stsDisc.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.stsSpeed.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.centralLayout.addLayout(self.infoLayout)

    def buildStatusBar(self):
        """  Create a status bar
        """
        self.logger.info(" Building Statusbar.")
        self.statusBar = self.statusBar()
        self.statusBar.setSizeGripEnabled(False)

        self.stsDate    = QLabel("Thursday 23 October 2025")
        self.stsBattery = QProgressBar()
        self.stsState   = QLabel("cisN")
        self.stsFrmt    = QLabel("L.E.D.")
        self.stsIdle    = QLabel("idle : 7s")

        self.stsDate.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.stsBattery.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stsState.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stsFrmt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stsIdle.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.statusBar.addPermanentWidget(self.stsDate,  1)
        self.statusBar.addPermanentWidget(self.stsBattery,  1)
        self.statusBar.addPermanentWidget(self.stsState, 1)
        self.statusBar.addPermanentWidget(self.stsFrmt, 1)
        self.statusBar.addPermanentWidget(self.stsIdle,  1)

        #self.stsBattery.setGeometry(0, 0, 8, 1)
        self.stsBattery.setFixedHeight(14)
        self.stsBattery.setFixedWidth(100)
        self.stsBattery.adjustSize()

    #  -------------------------------------------------------------------------------------------------------------------- toggleMenuBar -----------
    def toggleMenuBar(self):
        """  Toggles if the menu bar is displayed or not.
        """
        self.menu_bar = not self.menu_bar
        self.myMenu.setVisible(self.menu_bar)
        self.menu.actToggleMenuBar.setChecked(self.menu_bar)
    #  -------------------------------------------------------------------------------------------------------------------- toggleToolBar -----------
    def toggleToolBar(self):
        """  Toggles if the tool bar is displayed or not.
        """
        self.tool_bar = not self.tool_bar
        self.menu.toolbar.setVisible(self.tool_bar)
        self.menu.actToggleToolBar.setChecked(self.tool_bar)
    #  -------------------------------------------------------------------------------------------------------------------- openFontDialog ----------
    def openFontDialog(self):
        """  Open the font dialog.
        """
        font, ok = QFontDialog.getFont(self.txtTime.font(), self, "Choose Fomt for Time.")

        # If user clicked OK, update the label's font
        if ok:
            self.txtTime.setFont(font)
            self.timeFont = font
    # ----------------------------------------------------------------------------------------------------------------------- updateTime() ----------
    def updateTime(self):
        """  Update the time, info line  and status bar.
        """
        dtCurrent = QDateTime.currentDateTime()
        txtTime   = dtCurrent.toString("HH:mm:ss")
        txtDate   = dtCurrent.toString("dddd dd MMMM yyyy")

        self.nowTotalBytesReceived = self.systemInfo.TotalRawBytesReceived
        self.nowTotalBytesSent     = self.systemInfo.TotalRawBytesSent
        self.newTime               = time.time()
        deltaTime                  = self.newTime - self.lastTime

        downloadSpeed = (self.nowTotalBytesReceived - self.lastTotalBytesReceived) * 8 / deltaTime
        uploadSpeed   = (self.nowTotalBytesSent     - self.lastTotalBytesSent)     * 8 / deltaTime

        self.lastTotalBytesReceived = self.nowTotalBytesReceived
        self.lastTotalBytesSent     = self.nowTotalBytesSent
        self.lastTime               = self.newTime

        if self.timeMode == "Digital":
            self.lcdTime.display(txtTime)
            self.stsFrmt.setText("L.E.D.")
        else:
            self.timeFormat = self.menu.combo.currentText()
            self.updateTextTime()
            self.stsFrmt.setText(f"{self.timeFormat}")

        self.stsDate.setText(txtDate)
        self.stsState.setText(f"{utils.getState()}")
        if self.config.INFO_LINE:
            self.stsCPU.setText(f"CPU : {self.systemInfo.TotalCPUusage}")
            self.stsRAM.setText(f"RAM : {self.systemInfo.PercentageMemory}")
            self.stsDisc.setText(f"C: {utils.getDiscUsage()}")
            self.stsSpeed.setText(f"↓ {utils.formatSpeed(downloadSpeed)}  ↑ {utils.formatSpeed(uploadSpeed)}")
        self.stsIdle.setText(utils.getIdleDuration())

        self.updateBattery()

        if self.config.SOUNDS:
            self.sounds.playSounds(txtTime)
    # ----------------------------------------------------------------------------------------------------------------------- updateBattery() -------
    def updateBattery(self):
        """  Updates the battery icon in the status bar.

             The colour of the progress bar indicated the state of the battery.

             Running on mains      - light blue.
             battery low           - red
             Running on Battery    - yellow
             Battery charging      - blue
             Battery fully charged - green

        """
        state  = self.systemInfo.onBattery
        charge = self.systemInfo.batteryCharge

        match state:
            case True:
                if charge == 100:                           #  Fully Charged
                    self.stsBattery.setValue(charge)
                    self.stsBattery.setStyleSheet(self.pbStyles.BATTERY_FULL_STYLE)
                else:                                       #  Battery charging
                    self.stsBattery.setValue(charge)
                    self.stsBattery.setStyleSheet(self.pbStyles.CHARGING_STYLE)
            case False:                                     #  Running on battery
                self.stsBattery.setValue(charge)
                if charge < 10:
                        self.stsBattery.setStyleSheet(self.pbStyles.BATTERY_LOW_STYLE)
                else:
                    self.stsBattery.setStyleSheet(self.pbStyles.RUNNING_ON_BATTERY_STYLE)
            case _:
                self.stsBattery.setStyleSheet(self.pbStyles.RUNNING_ON_AC_STYLE)
    # ----------------------------------------------------------------------------------------------------------------------- updateTextTime() ------
    def updateTextTime(self):
        """  Updates the time text and if needed calls resizeWindow.

             The text time is bracketed with the prefix and postfix characters.  Mostly "".
        """

        textTime = f"{self.config.TIME_PREFIX}{self.selectTime.getTime(self.timeFormat)}{self.config.TIME_POSTFIX}"

        if self.config.TIME_SPACE != " ":
            textTime = textTime.replace(" ", self.config.TIME_SPACE)

        self.txtTime.setText(textTime)
        self.txtWidth  = self.txtTime.fontMetrics().boundingRect(self.txtTime.text()).width()
        self.txtHeight = self.txtTime.fontMetrics().boundingRect(self.txtTime.text()).height()
        #infoLineWidth  = self.infoLayout.geometry().width()
        statbarWidth   = self.statusBar.geometry().width()

        if self.txtWidth > statbarWidth:
            if self.txtWidth != self.lblWidth or self.txtHeight != self.lblHeight:
                self.resizeWindow()
    # ----------------------------------------------------------------------------------------------------------------------- resizeWindow() --------
    def resizeWindow(self):
        """  Resizes the main window.
             Will align to the side of the screen if required.
             Will only align to the primary screen, I think - I only have one screen
        """
        self.lblWidth  = self.txtWidth              #  Saved to be used in updateTextTime.
        self.lblHeight = self.txtHeight             #  Saved to be used in updateTextTime.
        self.width     = self.lblWidth
        self.height    = self.lblHeight
        if self.config.TOOL_BAR:
            self.height += 40

        screenSize = QApplication.primaryScreen().availableGeometry()

        if self.config.TIME_ALIGNMENT:
            match self.config.TIME_ALIGNMENT:
                case "Left":                                                                        #  align to left hand of the screen.
                    self.setGeometry(5, self.Ypos, self.width, self.height)
                case "Right":                                                                       #  align to right hand of the screen.
                    xpos = screenSize.width()-self.width-30
                    self.setGeometry(xpos, self.Ypos, self.width, self.height)
        else:
            self.setGeometry(self.Xpos, self.Ypos, self.width, self.height)
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
            self.myMenu.setStyleSheet(f"color: {self.foregroundColour}")
            if self.config.INFO_LINE:
                self.stsCPU.setStyleSheet(f"color: {self.foregroundColour}")
                self.stsRAM.setStyleSheet(f"color: {self.foregroundColour}")
                self.stsDisc.setStyleSheet(f"color: {self.foregroundColour}")
                self.stsSpeed.setStyleSheet(f"color: {self.foregroundColour}")
            self.menu.toolbar.setStyleSheet(f"color: {self.foregroundColour}")
            self.menu.context_menu.setStyleSheet(f"color: {self.foregroundColour}")

            return

        self.centralWidget.setStyleSheet(f"color: {self.foregroundColour}; background-color: {self.backgroundColour}; margin:0px; border:0px")
        if self.config.INFO_LINE:
            self.infoLayout.setStyleSheet(f"color: {self.foregroundColour}; background-color: {self.backgroundColour}; margin:0px; border:0px")
        self.statusBar.setStyleSheet(f"color: {self.foregroundColour}; background-color: {self.backgroundColour}")
        self.myMenu.setStyleSheet(f"color: {self.foregroundColour}; background-color: {self.backgroundColour}")
        self.menu.toolbar.setStyleSheet(f"color: {self.foregroundColour}; background-color: {self.backgroundColour}")
        self.menu.context_menu.setStyleSheetf(f"color: {self.foregroundColour}; background-color: {self.backgroundColour}")
    # ----------------------------------------------------------------------------------------------------------------------- setDigitalTime() ------
    def setDigitalTime(self):
        """  Bring forward the digital time display, hides the text time display.
        """
        self.stackedLayout.setCurrentIndex(0)
        self.timeMode = "Digital"
    # ----------------------------------------------------------------------------------------------------------------------- setWordTime() ---------
    def setTextTime(self):
        """  Bring forward the text time display, hides the digital time display.
        """
        self.stackedLayout.setCurrentIndex(1)
        self.timeMode = "Text"
    # ----------------------------------------------------------------------------------------------------------------------- getForeColour() -------
    def getForeColour(self):
        """  launch the colour input dialog and obtain the new foreground colour.
        """
        current_color = QColor(self.foregroundColour)
        colour = QColorDialog.getColor(current_color, self, "Choose Foreground Colour")
        if colour.isValid():
            self.foregroundColour = colour.name()
            self.updateColour()
    # ----------------------------------------------------------------------------------------------------------------------- getBackColour() -------
    def getBackColour(self):
        """  launch the colour input dialog and obtain the new background colour.
        """
        current_color = QColor(self.backgroundColour)
        colour = QColorDialog.getColor(current_color, self, "Choose Background Colour")
        if colour.isValid():
            self.backgroundColour = colour.name()
            self.updateColour()
    # ----------------------------------------------------------------------------------------------------------------------- mousePressEvent -------
    #  The three following methods are in place of the default mouse events - so pyKlock can be dragged
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
        self.Xpos = self.x()
        self.Ypos = self.y()
    # ----------------------------------------------------------------------------------------------------------------------- openTextFile ----------
    def openHelpFile(self):
        """  Open a text viewer.
        """
        if self.helpWindow is None:
            self.helpWindow = hp.HelpViewer(self)
            self.helpWindow.show()
    # ----------------------------------------------------------------------------------------------------------------------- openTextFile ----------
    @pyqtSlot()
    def openTextFile(self):
        """  Open a text viewer.
        """
        action = self.sender()

        if self.textWindow is None:
            self.textWindow = tw.TextViewer(self, action.text(), self.logger)
            self.textWindow.show()
    # ----------------------------------------------------------------------------------------------------------------------- openAbout -------------
    def openAbout(self, event):
        """  Open an About window, which display application, system information and run times.
        """
        dlg = About.About(self, self.config, self.logger, self.startTime)
        dlg.exec()
    #  ---------------------------------------------------------------------------------------------------------------------- openSettings ----------
    def openSettings(self):
        """  Open an Setting window, which displays the settings available to pyKlock and allows them to be amended.
        All button processing, settings saving and validation is handled withing the dialog.
        """
        dlg = stngs.Settings(self, self.config, self.logger)
        dlg.exec()

        self.updateValues()         #  not sure if config has changes - so, update.
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        """  Ask for confirmation before closing, if required.

             Save new config properties to file.
        """
        if self.config.CONFIRM_EXIT:
            confirmation = QMessageBox.question(self, "Confirmation", "Are you sure you want to close the application?")

            if confirmation == QMessageBox.StandardButton.Yes:
                self.endBit()
                event.accept()      #  Close the app.
            else:
                event.ignore()      #  Continue the app.
        else:
            self.endBit()
            event.accept()          #  Close the app.
            self.close()
    # ----------------------------------------------------------------------------------------------------------------------- endBit() --------------
    def endBit(self):
        """  Save config file, stop the timer and print Goodbye.
        """
        self.timer.stop()           #  Stop the time when the frame closes.
        self.timer = None           #  Hopefully, stop any memory leaks - maybe only need close()
        self.saveConfig()
        self.logger.info(f"  Ending {self.config.NAME} Version {self.config.VERSION} ")
        self.logger.info("=" * 100)
    # ----------------------------------------------------------------------------------------------------------------------- saveConfig() ----------
    def saveConfig(self):
        """  Save stuff to the config file, in case any has changed.
        """
        self.config.X_POS       = self.Xpos
        self.config.Y_POS       = self.Ypos
        self.config.WIDTH       = self.width
        self.config.HEIGHT      = self.height
        self.config.MENU_BAR    = self.menu_bar
        self.config.TOOL_BAR    = self.tool_bar
        self.config.TIME_MODE   = self.timeMode
        self.config.TIME_FONT   = self.timeFont.toString()
        self.config.TIME_FORMAT = self.timeFormat
        self.config.TRANSPARENT = self.transparent
        self.config.FOREGROUND  = self.foregroundColour
        self.config.BACKGROUND  = self.backgroundColour
        self.config.writeConfig()
    # ----------------------------------------------------------------------------------------------------------------------- contextMenuEvent() ----
    def contextMenuEvent(self, event):
        """  ** NEEDED for the context menu to work **

             This overrides a system method, so the context menu is executed.
        """
        # Show the context menu
        self.menu.context_menu.exec(event.globalPos())
