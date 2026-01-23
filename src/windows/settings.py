###############################################################################################################
#    Settings   Copyright (C) <2025-26>  <Kevin Scott>                                                        #
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
                             QApplication, QLineEdit, QPushButton, QColorDialog, QComboBox, QFontDialog,
                             QMessageBox, QSlider, QCheckBox)
from PyQt6.QtGui     import QIcon, QColor, QFont
from PyQt6.QtCore    import Qt

from src.classes.QToggle import QToggle

import src.classes.sounds as snds
import src.classes.styles as styles
import src.classes.selectTime as st

from src.projectPaths import RESOURCE_PATH

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
        self.styles = styles.Styles()             #  Styles for QToggle.
        self.sounds = snds.Sounds(self.config, self.logger)

        self.height = 400
        self.width  = 460
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
        self.newSettings      = {}              # a directory to hold amended settings if any.

        layout = QVBoxLayout()

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.clicked.connect(self.buttonClicked)

        self.twTab = QTabWidget()

        funcs = [self.Info, self.Application, self.Display, self.Time, self.Sound]

        for func in funcs:          #  Add the individual tabs.  For a tab to be added - insert title into the list funcs.
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
        layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
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

             NB : application x, y, width & height - are stored as int, but display as strings.
        """
        page = QWidget(self.twTab)
        layout = QFormLayout()
        page.setLayout(layout)

        titles   = ["X Position - Main Window ", "Y Position - Main Window ", "Width - Main Window ", "Height - Main Window "]
        settings = ["X_POS", "Y_POS", "WIDTH", "HEIGHT"]

        for le in zip(titles, settings, strict=True):
            title   = le[0]
            setting = le[1]

            value    = self.config.__getattribute__(setting)       #  Dirty way of getting the property value using a string.
            lineEdit = QLineEdit(str(value), self)
            lineEdit.setObjectName(setting)
            lineEdit.editingFinished.connect(self.appSettingsUpdate)

            layout.addRow(title, lineEdit)

        # create toggle buttons.
        self.tgToolBar = QToggle(self)
        self.tgToolBar.setChecked(self.config.TOOL_BAR)
        self.tgToolBar.stateChanged.connect(self.appSettingsUpdate)
        self.tgToolBar.setObjectName("TOOL_BAR")
        self.tgToolBar.setStyleSheet(self.styles.QToggle_STYLE)

        self.tgConfirmExit = QToggle(self)
        self.tgConfirmExit.setChecked(self.config.CONFIRM_EXIT)
        self.tgConfirmExit.stateChanged.connect(self.appSettingsUpdate)
        self.tgConfirmExit.setObjectName("CONFIRM_EXIT")
        self.tgConfirmExit.setStyleSheet(self.styles.QToggle_STYLE)

        layout.addRow("Display Tool Bar ", self.tgToolBar)
        layout.addRow("Confirm Exit ",     self.tgConfirmExit)

        self.twTab.addTab(page, "Application Data")

    def appSettingsUpdate(self, checked=None):
        """  When a line edit or combo boxes are changed and looses focus, add amended value to new Settings dictionary.
        """
        action = self.sender()
        name   = action.objectName()

        match name:
            case "X_POS" | "Y_POS" | "WIDTH" | "HEIGHT":        #  colour dialog
                self.newSettings[name] = int(action.text())
            case "CONFIRM_EXIT", "TOOL_BAR":
                checked = not checked
                self.btnConfirmExit.setDefault(checked)
                self.newSettings[name] = checked
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
        self.btnForeColour.clicked.connect(self.displaySettingsUpdate)
        self.btnForeColour.setObjectName("FOREGROUND")
        path = f"{RESOURCE_PATH}/colour-swatch.png"
        self.btnBackColour = QPushButton()
        self.btnBackColour.setIcon(QIcon(path))
        self.btnBackColour.setStyleSheet(f"background-color: {self.backgroundColour}")
        self.btnBackColour.clicked.connect(self.displaySettingsUpdate)
        self.btnBackColour.setObjectName("BACKGROUND")

        leTransparent = QLineEdit("Amend in config.toml and restart", self)
        leTransparent.setReadOnly(True)

        self.tgInfoLine = QToggle(self)
        self.tgInfoLine.setChecked(self.config.INFO_LINE)
        self.tgInfoLine.stateChanged.connect(self.displaySettingsUpdate)
        self.tgInfoLine.setObjectName("INFO_LINE")
        self.tgInfoLine.setStyleSheet(self.styles.QToggle_STYLE)

        layout.addRow("Foreground Colour ", self.btnForeColour)
        layout.addRow("Background Colour ", self.btnBackColour)
        layout.addRow("Transparent Background ", leTransparent)
        layout.addRow("Information Line ", self.tgInfoLine)

        self.twTab.addTab(page, "Display")

    def displaySettingsUpdate(self, checked=None):
        """  When a line edit or combo boxes are changed and looses focus, add amended value to new Settings dictionary.
        """
        action = self.sender()
        name   = action.objectName()

        match name:
            case "FOREGROUND" | "BACKGROUND":        #  colour dialog
                self.current_color = QColor(self.foregroundColour)
                colour = QColorDialog.getColor(self.current_color, self, f"Choose {name} Colour")

                if colour.isValid():
                    if name == "FOREGROUND":
                        self.foregroundColour = colour.name()
                        self.newSettings[name] = self.foregroundColour
                    else:
                        self.backgroundColour = colour.name()
                        self.newSettings[name] = self.backgroundColour
            case "INFO_LINE":
                checked = not checked
                self.tgInfoLine.setChecked(checked)
                self.newSettings[name] = checked
    # ----------------------------------------------------------------------------------------------------------------------- Time() ----------------
    def Time(self):
        page = QWidget(self.twTab)
        layout = QFormLayout()
        page.setLayout(layout)

        self.cbTimeMode = QComboBox()
        self.cbTimeMode.insertItems(1, ["Digital", "Text"])
        self.setText(self.cbTimeMode,   self.config.TIME_MODE)
        self.cbTimeMode.currentTextChanged.connect(self.timeSettingsUpdate)
        self.cbTimeMode.setObjectName("TIME_MODE")
        self.cbTimeFmt = QComboBox()
        self.cbTimeFmt.insertItems(1, self.selectTime.timeTypes)
        self.setText(self.cbTimeFmt,    self.config.TIME_FORMAT)
        self.cbTimeFmt.currentTextChanged.connect(self.timeSettingsUpdate)
        self.cbTimeFmt.setObjectName("TIME_FORMAT")
        self.cbTimeAlign = QComboBox()
        self.cbTimeAlign.insertItems(1, ["Left", "Right", "None"])
        self.setText(self.cbTimeAlign, self.config.TIME_ALIGNMENT)
        self.cbTimeAlign.currentTextChanged.connect(self.timeSettingsUpdate)
        self.cbTimeAlign.setObjectName("TIME_ALIGNMENT")

        # create a button.
        path = f"{RESOURCE_PATH}/font.png"
        self.btnFont = QPushButton()
        self.btnFont.setIcon(QIcon(path))
        self.btnFont.setObjectName("TIME_FONT")
        self.btnFont.clicked.connect(self.timeSettingsUpdate)

        layout.addRow("Time Format ",      self.cbTimeMode)
        layout.addRow("Text Time Format ", self.cbTimeFmt)
        layout.addRow("Time Font ",        self.btnFont)
        layout.addRow("Time Alignment ",  self.cbTimeAlign)

        titles   = ["Prefix Character ", "Postfix Character ", "Space Character "]
        settings = ["TIME_PREFIX", "TIME_POSTFIX", "TIME_SPACE"]

        for le in zip(titles, settings, strict=True):
            title   = le[0]
            setting = le[1]

            value    = self.config.__getattribute__(setting)       #  Dirty way of getting the property value using a string.
            lineEdit = QLineEdit(str(value), self)
            lineEdit.setObjectName(setting)
            lineEdit.editingFinished.connect(self.timeSettingsUpdate)
            lineEdit.setStyleSheet(self.styles.QEdit_STYLE)

            layout.addRow(title, lineEdit)

        self.twTab.addTab(page, "Time")

    def setText(self, combo, text):
        """  Sets the combo to display the given text.
             The values of the combobox is searched for the index and this is used to set the text.
             If the text is not found, the index is set to 1.
        """
        index = combo.findText(text)
        if index < 0:                   #  If text not found, index will be -1.
            index = 0

        combo.setCurrentIndex(index)

    def timeSettingsUpdate(self):
        """  When a line edit or combo boxes are changed and looses focus, add amended value to new Settings dictionary.
        """
        action = self.sender()
        name   = action.objectName()

        match name:
            case "TIME_MODE" | "TIME_FORMAT" | "TIME_ALIGNMENT":        #  combo boxes
                self.newSettings[name] = action.currentText()
            case "TIME_PREFIX" | "TIME_POSTFIX" | "TIME_SPACE":         #  line edits
                self.newSettings[name] = action.text()
            case "TIME_FONT":
                font, ok = QFontDialog.getFont(self.timeFont, self, "Choose Font for Time Text.")

                # If user clicked OK, update the label's font
                if ok:
                    self.timeFont = font.toString()
                    self.newSettings[name] = self.timeFont
    # ----------------------------------------------------------------------------------------------------------------------- Time() ----------------
    def Sound(self):
        page = QWidget(self.twTab)
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        page.setLayout(layout)

        volume = self.config.SOUNDS_VOLUME
        self.toggles =  {}
        titles   = ["Play Sounds ", "Westminster Chimes ", "Chimes on the Hour ", "Chimes on the Quarter", "Play pips on the Hour", "Cuckoo Chimes"]
        settings = ["SOUNDS", "SOUNDS_WESTMINSTER", "SOUNDS_HOUR_CHIMES", "SOUNDS_QUARTER_CHIMES", "SOUNDS_HOUR_PIPS", "SOUNDS_CUCKOO"]

        for le in zip(titles, settings, strict=True):
            title   = le[0]
            setting = le[1]

            value = self.config.__getattribute__(setting)       #  Dirty way of getting the property value using a string.
            checked = True if value else False

            self.toggles[setting] = QToggle(self)
            self.toggles[setting].setChecked(checked)
            self.toggles[setting].stateChanged.connect(self.displaySoundUpdate)
            self.toggles[setting].setObjectName(setting)
            self.toggles[setting].setStyleSheet(self.styles.QToggle_STYLE)

            layout.addRow(title, self.toggles[setting])

        self.sldVolume = QSlider(Qt.Orientation.Horizontal, self)
        self.sldVolume.setSingleStep(1)
        self.sldVolume.setRange(0, 100)
        self.sldVolume.setValue(volume)
        self.sldVolume.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.sldVolume.valueChanged.connect(self.displaySoundUpdate)
        self.sldVolume.setObjectName("SOUNDS_VOLUME")

        self.btnVolume = QPushButton()
        self.btnVolume.setObjectName("TEST_VOLUME")
        self.btnVolume.clicked.connect(self.displaySoundUpdate)

        layout.addRow(f"Volume ", self.sldVolume)
        layout.addRow(f"Test Volume ", self.btnVolume)

        self.twTab.addTab(page, "Sound")

    def displaySoundUpdate(self, checked=None):
        """
        """
        action = self.sender()
        name   = action.objectName()
        
        match name:
            case "SOUNDS_VOLUME":
                self.newSettings[name] = self.sldVolume.value()
            case "TEST_VOLUME":
                self.testVolume()
            case _:
                checked = True if checked == 2 else False
                self.toggles[name].setChecked(checked)
                self.newSettings[name] = checked

    def testVolume(self):
        """  Plays the Pips at the slider volume to test loudness.
        """
        self.sounds.playPips(self.sldVolume.value())
    # ----------------------------------------------------------------------------------------------------------------------- buttonClicked() -------
    def buttonClicked(self, button):
        """   Handles the pressed buttons, either Ok or Cancel.
              All button processing, settings saving and validation is handled within this class.

              If Ok is pressed the new settings are written to the config file.
              if Cancel is pressed the form will just close.
                 If amendments have been made, they are lost - prompt the user first.
        """
        role = self.buttonBox.standardButton(button)
        if role == QDialogButtonBox.StandardButton.Cancel:
            if self.newSettings:                        #  Settings have been amended.
                confirmation = QMessageBox.question(self, "Confirmation", "Are you sure you want to close the application?")

                if confirmation == QMessageBox.StandardButton.Yes:
                    self.close()                        #  Close the app, losing any edits.
                else:
                    return                              #  Continue to the app.
            else:                                       #  No settings have been amended.
                self.close()                            #  Close the app.

        elif role == QDialogButtonBox.StandardButton.Ok:
            self.saveSettings()
            self.close()
    # ----------------------------------------------------------------------------------------------------------------------- saveSettings() --------
    def saveSettings(self):
        """  Transfers the new settings dictionary to config values and writes new config file.
        """
        for key, value in self.newSettings.items():
            print(f"key = {key} :: val = {value}")
            self.config.__setattr__(key, value)         #  Dirty way of setting the property value using a string.

        self.newSettings = {}                           #  Clear new settings dict
        self.config.writeConfig()                       #  Save new settings.
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        self.logger.info("Settings Close Event")
        event.accept()


