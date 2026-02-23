###############################################################################################################
#    infoViewer   Copyright (C) <2026>  <Kevin Scott>                                                         #
#                                                                                                             #
#    A generic viewer for various info views.                                                                 #
#    The info module should provide a buildGUI method                                                         #
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

import src.info.easterInfo as estr
import src.info.NTPInfo as ntp

from PyQt6.QtWidgets import QApplication, QMainWindow

import src.classes.styles as styles

class easterViewer(QMainWindow):
    """  Display results from a number of info modules in a separate window.
    """
    def __init__(self, myLogger, myConfig, info):
        super().__init__()

        self.logger = myLogger
        self.config = myConfig
        self.styles = styles.Styles()

        self.height      = 400
        self.width       = 400
        self.screenSize  = QApplication.primaryScreen().availableGeometry()
        self.xPos        = int((self.screenSize.width() / 2)  - (self.width / 2))
        self.yPos        = int((self.screenSize.height() / 2) - (self.height / 2))

        self.setGeometry(self.xPos, self.yPos, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle(info)

        match info:
            case "Easter Dates":
                estr.buildGUI(self)
                estr.update(self)
            case "NTP Server":
                ntp.buildGUI(self)
                
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        """  When the viewer is closed, checks if any child windows are still open.
        """
        ntp.close(self)
        event.accept()


