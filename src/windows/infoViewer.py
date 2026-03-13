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

import src.info.chineseYearInfo as cny
import src.info.publicHolidays as ph
import src.info.equinoxInfo as ei
import src.info.worldKlock as wk
import src.info.NTPInfo as ntp

from PyQt6.QtWidgets import QApplication, QMainWindow


class infoViewer(QMainWindow):
    """  Display results from a number of info modules in a separate window.

         If the view uses a timer, set timerStarted to True, so the time can be stopped when the viewer is closed.
    """
    def __init__(self, myLogger, myConfig, info):
        super().__init__()

        self.logger = myLogger
        self.config = myConfig
        
        self.setWindowTitle(info)  
        
        match info:
            case "Public Holidays":
                self.setWindow(500, 500)
                ph.init(self)
                ph.buildGUI(self)
                ph.update(self)
            case "NTP Server":
                self.setWindow(400, 500)
                self.timerStarted = True
                ntp.buildGUI(self)
                ntp.update(self)
            case "Chinese New Year":
                self.setWindow(500, 500)
                cny.buildGUI(self)
                cny.update(self)
            case "Season Equinox":
                self.setWindow(500, 500)
                ei.buildGUI(self)
            case "World Klock":
                self.setWindow(600, 500)
                self.timerStarted = True
                wk.buildGUI(self)
                wk.update(self)

    # ----------------------------------------------------------------------------------------------------------------------- setWindow() -----------
    def setWindow(self, width, height):  
        """  Set the x position, y position, width and height of the Info Viewer.
        """   
        self.height       = height
        self.width        = width
        self.screenSize   = QApplication.primaryScreen().availableGeometry()
        self.xPos         = int((self.screenSize.width() / 2)  - (self.width / 2))
        self.yPos         = int((self.screenSize.height() / 2) - (self.height / 2))
        self.timerStarted = False

        self.setGeometry(self.xPos, self.yPos, self.width, self.height)
        self.setFixedSize(self.width, self.height)
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        """  When the viewer is closed, checks if any child windows are still open.
        """
        if self.timerStarted:
            self.timerStarted = False
            ntp.close(self)
            wk.close(self)
        event.accept()


