###############################################################################################################
#    sounds.py   Copyright (C) <2024-26>  <Kevin Scott>                                                       #
#    For changes see history.txt                                                                              #
#                                                                                                             #
#    A class for managing sounds.                                                                             #
#                                                                                                             #
#    23 January 2026 - Amended playPips to play at a given volume.                                            #
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
#      import src.classes.sounds as snds                                                                      #
#                                                                                                             #
#      self.sounds      = snds.Sounds(self.myConfig)                                                          #
#                                                                                                             #
#      self.sounds.playSounds()  - will play sounds depending upon options.                                   #
#                                                                                                             #
#      Current options -                                                                                      #
#                       Play chimes ever hour.                                                                #
#                       Play chimes ever quarter.                                                             #
#                       Play the pips on the hour.                                                            #
#                                                                                                             #
#      Probably needs volume control.                                                                         #
#                                                                                                             #
#    You should have received a copy of the GNU General Public License along with this program.               #
#    If not, see <http://www.gnu.org/licenses/>.                                                              #
#                                                                                                             #
###############################################################################################################

from audioplayer import AudioPlayer

from PyQt6.QtWidgets import (QMessageBox)

import src.projectPaths as pp


class Sounds():
    """  A class for managing sounds.

         Should only be called if config setting is set to True.

         If SOUNDS_HOUR_CHIMES is called then Westminster type chimes are played on the hour.
         If SOUNDS_QUARTER_CHIMES is called then Westminster type chimes are played on the quarter hour.
         If SOUNDS_HOUR_PIPS is called then the BBC type pips are played on the hour.
    """

    def __init__(self, myConfig, myLogger):
        self.myConfig = myConfig
        self.myLogger = myLogger

        self.hour        = True
        self.quarterPast = True
        self.halfPast    = True
        self.quarterTo   = True

        self.strHour = {
            0  : "twelve",
            1  : "one",
            2  : "two",
            3  : "three",
            4  : "four",
            5  : "five",
            6  : "six",
            7  : "seven",
            8  : "eight",
            9  : "nine",
            10 : "ten",
            11 : "eleven",
            12 : "twelve"}

        self.checkHourChimes()
# ------------------------------------------------------------------------------------- playSounds ----------------------
    def playSounds(self, timeText):
        """  Called to play the actual sounds.
             The config file should of been read in __init__.
        """
        hours    = int(timeText[0:2])
        minutes  = int(timeText[3:5])
        sndPath  = ""

        if hours > 12:
            hours -= 12                         #  Work on a 12 hour klock.

        if self.myConfig.SOUNDS_HOUR_CHIMES and self.hour:
            if minutes == 0:
                self.hour = False
                if self.myConfig.SOUNDS_WESTMINSTER:
                    sndPath = f"{pp.RESOURCE_PATH}\\Sounds\\westminster\\{self.strHour[hours]}.mp3"
                if self.myConfig.SOUNDS_CUCKOO:
                    sndPath = f"{pp.RESOURCE_PATH}\\Sounds\\cuckoo\\{self.strHour[hours]}.mp3"
                if self.myConfig.SOUNDS_HOUR_PIPS:
                    sndPath = f"{pp.RESOURCE_PATH}\\Sounds\\thepips.mp3"

        if self.myConfig.SOUNDS_QUARTER_CHIMES:
            if minutes in [15, 30, 45]:
                match minutes:
                    case 15:
                        if self.quarterPast:
                            self.quarterPast = False
                            sndPath          = f"{pp.RESOURCE_PATH}\\Sounds\\westminster\\quarterchime.mp3"
                    case 30:
                        if self.halfPast:
                            self.halfPast = False
                            sndPath       = f"{pp.RESOURCE_PATH}\\Sounds\\westminster\\halfchime.mp3"
                    case 45:
                        if self.quarterTo:
                            self.quarterTo = False
                            sndPath        = f"{pp.RESOURCE_PATH}\\Sounds\\westminster\\threequarterchime.mp3"
        if sndPath:
            # Playback stops when the object is destroyed (GC"ed), so save a reference to the object for non-blocking playback.
            try:
                self.player = AudioPlayer(sndPath)
                self.player.volume = self.myConfig.SOUNDS_VOLUME
                self.player.play(block=False)
            except Exception as e:
                self.myLogger.error(f"Error {e}")

        if minutes == 2:
            self.hour        = True
            self.quarterPast = True
            self.halfPast    = True
            self.quarterTo   = True
# ------------------------------------------------------------------------------------- playPips ------------------------
    def playPips(self, volume):
        """  Enable the pip to be played to test the volume.
        """
        try:
            player = AudioPlayer(f"{pp.RESOURCE_PATH}\\Sounds\\thepips.mp3")
            player.volume = volume
            player.play(block=True)
        except Exception as e:
            self.myLogger.error(f"Error {e}")
# ------------------------------------------------------------------------------------- checkHourChimes -----------------
    def checkHourChimes(self):
        """  There should be one and only one hour chime selected.
             This should not happen, but check anyway.
        """
        clash = 0
        if self.myConfig.SOUNDS_WESTMINSTER:
            clash += 1

        if self.myConfig.SOUNDS_CUCKOO:
            clash += 1

        if self.myConfig.SOUNDS_HOUR_PIPS:
            clash += 1

        if clash < 2:                       #  Only one hour chime selected - all okay.
            return

        #  A bit of a work around, I use a QMessageBox but customise the button texts.
        msg = QMessageBox()
        msg.setWindowTitle("Hour Chime")
        msg.setText("More then one Hour chime selected")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Ok)
        buttonY = msg.button(QMessageBox.StandardButton.Yes)
        buttonY.setText("Westminster")
        buttonN = msg.button(QMessageBox.StandardButton.No)
        buttonN.setText("Cuckoo")
        buttonO = msg.button(QMessageBox.StandardButton.Ok)
        buttonO.setText("Pips")
        msg.exec()

        response = msg.clickedButton().text()

        match response:
            case "Westminster":
                self.myConfig.SOUNDS_WESTMINSTER = True
                self.myConfig.SOUNDS_HOUR_CHIMES = True
                self.myConfig.SOUNDS_CUCKOO      = False
                self.myConfig.SOUNDS_HOUR_PIPS   = False
            case "Cuckoo":
                self.myConfig.SOUNDS_WESTMINSTER = False
                self.myConfig.SOUNDS_CUCKOO      = True
                self.myConfig.SOUNDS_HOUR_PIPS   = False
            case "Pips":
                self.myConfig.SOUNDS_WESTMINSTER = False
                self.myConfig.SOUNDS_CUCKOO      = False
                self.myConfig.SOUNDS_HOUR_PIPS   = True

        self.myConfig.writeConfig()


