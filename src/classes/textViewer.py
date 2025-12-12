###############################################################################################################
#    TextViewer.py    Copyright (C) <2025>  <Kevin Scott>                                                     #
#                                                                                                             #
#    A class that displays a text file in a separate window.                                                  #
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

from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QPlainTextEdit

from src.projectPaths import MAIN_PATH, LOGGER_PATH


class TextViewer(QWidget):
    """  A class that displays a text file in a separate window.
    """
    def __init__(self, parent, action, logger):
        super().__init__()

        self.setWindowTitle("pyKlock Licence")
        self.setGeometry(300, 300, 800, 400)

        self.parent = parent
        self.action = action
        self.logger = logger

        self.buildGUI()
        self.loadText()

    def buildGUI(self):
        """  Build the GUI elements.
        """
        self.textEdit = QPlainTextEdit()

        btnClose = QPushButton(text="Close", parent=self)
        btnClose.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(btnClose)

        self.setLayout(layout)

    def loadText(self):
        """  Load the text file.
             The text file can be either Licence ot Log File.
        """
        match self.action:
            case "Licence":
                self.textFile = f"{MAIN_PATH}/LICENCE.txt"
            case "Log File":
                self.textFile = f"{LOGGER_PATH}"
            case "_":
                self.logger.error(" ERROR - Unknown text file type.")

        with open(self.textFile) as tFile:       # In context manager.
            text = tFile.read()
        self.textEdit.setPlainText(text)

    def closeEvent(self, event):
        self.parent.textWindow = None       #  Set to None in parent, so can open TextViewer again.
        event.accept()
