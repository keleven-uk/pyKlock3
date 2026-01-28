###############################################################################################################
#    myConfig.py    Copyright (C) <2025-26>  <Kevin Scott>                                                    #
#                                                                                                             #
#    A class that acts has a wrapper around the configure file - config.toml.                                 #
#    The configure file is first read, then the properties are made available.                                #
#    The configure file is currently in toml format.                                                          #
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

import datetime

import toml


class Config():
    """  A class that acts has a wrapper around the configure file - config.toml.
         The configure file is hard coded and lives in the same directory has the main script.
         The configure file is first read, then the properties are made available.

         If config.toml is not found, a default configure file is generated.

         The get read the directory and if the key is not found a default is returned.

         usage:
            myConfig = myConfig.Config()
    """

    def __init__(self, CONFIG_PATH, logger):

        self.FILE_NAME = CONFIG_PATH
        self.logger    = logger

        try:
            with open(self.FILE_NAME, "r") as configFile:       # In context manager.
                self.config = toml.load(configFile)             # Load the configure file, in toml.
        except FileNotFoundError:
            self.logger.debug("Configure file not found.")
            self.logger.debug("Writing default configure file.")
            self._writeDefaultConfig()
            self. logger.debug("Running program with default configure settings.")
        except toml.TomlDecodeError:
            self.logger.debug("Error reading configure file.")
            self.logger.debug("Writing default configure file.")
            self._writeDefaultConfig()
            self.logger.debug("Running program with default configure settings.")


    @property
    def NAME(self):
        """  Returns the application name.
        """
        return self.config["INFO"].get("myNAME", "pyKlock")

    @property
    def VERSION(self):
        """  Returns the application Version.
        """
        return self.config["INFO"]["myVERSION"]

    @property
    def FOREGROUND(self):
        """  Returns the window foreground colour.
        """
        value = self.config["DISPLAY"].get("foreground", "#00ff00")
        return value

    @FOREGROUND.setter
    def FOREGROUND(self, value):
        """  Sets the window foreground colour.
        """
        self.config["DISPLAY"]["foreground"] = value

    @property
    def BACKGROUND(self):
        """  Returns the window background colour.
        """
        value = self.config["DISPLAY"].get("background", "#000000")
        return value

    @BACKGROUND.setter
    def BACKGROUND(self, value):
        """  Sets the window background colour.
        """
        self.config["DISPLAY"]["background"] = value

    @property
    def TRANSPARENT(self):
        """  Returns if the window should be transparent.
        """
        return self.config["DISPLAY"].get("transparent", True)

    @TRANSPARENT.setter
    def TRANSPARENT(self, value):
        """  Sets if the window should be transparent.
        """
        self.config["DISPLAY"]["transparent"] = value

    @property
    def INFO_LINE(self):
        """  Returns if the window should be transparent.
        """
        return self.config["DISPLAY"].get("infoLine", True)

    @INFO_LINE.setter
    def INFO_LINE(self, value):
        """  Sets if the window should be transparent.
        """
        self.config["DISPLAY"]["infoLine"] = value

    @property
    def X_POS(self):
        """  Returns the X co-ordinate of the top right hand corner of the window.
        """
        return self.config["APPLICATION"].get("x_pos", "0")

    @X_POS.setter
    def X_POS(self, value):
        """  Sets the X co-ordinate of the top right hand corner of the window.
        """
        self.config["APPLICATION"]["x_pos"] = value

    @property
    def Y_POS(self):
        """  Returns the Y co-ordinate of the top right hand corner of the window.
        """
        return self.config["APPLICATION"].get("y_pos", "0")

    @Y_POS.setter
    def Y_POS(self, value):
        """  Sets the Y co-ordinate of the top right hand corner of the window.
        """
        self.config["APPLICATION"]["y_pos"] = value

    @property
    def WIDTH(self):
        """  Returns the window width.
        """
        return self.config["APPLICATION"].get("width", "400")

    @WIDTH.setter
    def WIDTH(self, value):
        """  Sets the window width.
        """
        self.config["APPLICATION"]["width"] = value

    @property
    def HEIGHT(self):
        """  Returns the window height.
        """
        return self.config["APPLICATION"].get("height", "200")

    @HEIGHT.setter
    def HEIGHT(self, value):
        """  Sets the window height.
        """
        self.config["APPLICATION"]["height"] = value

    @property
    def CONFIRM_EXIT(self):
        """  Returns if confirmation is needed on exit.
        """
        return self.config["APPLICATION"].get("confirmExit", False)

    @CONFIRM_EXIT.setter
    def CONFIRM_EXIT(self, value):
        """  Sets if confirmation is needed on exit.
        """
        self.config["APPLICATION"]["confirmExit"] = value

    @property
    def MENU_BAR(self):
        """  Returns if the menu bar is displayed.
        """
        return self.config["APPLICATION"].get("menuBar", True)

    @MENU_BAR.setter
    def MENU_BAR(self, value):
        """  Sets if the menu bar is displayed.
        """
        self.config["APPLICATION"]["menuBar"] = value

    @property
    def TOOL_BAR(self):
        """  Returns if the tool bar is displayed.
        """
        return self.config["APPLICATION"].get("toolBar", True)

    @TOOL_BAR.setter
    def TOOL_BAR(self, value):
        """  Sets if the tool bar is displayed.
        """
        self.config["APPLICATION"]["toolBar"] = value

    @property
    def TIME_MODE(self):
        """  Returns the Time mode.
             Either Digital of Text.
        """
        return self.config["TIME"].get("mode", "Digital")

    @TIME_MODE.setter
    def TIME_MODE(self, value):
        """  Sets the Time mode.
             Either Digital of Text.
        """
        self.config["TIME"]["mode"] = value

    @property
    def TIME_FORMAT(self):
        """  Returns the Time format.
        """
        return self.config["TIME"].get("format", "Fuzzy Time")

    @TIME_FORMAT.setter
    def TIME_FORMAT(self, value):
        """  Sets the Time format.
        """
        self.config["TIME"]["format"] = value

    @property
    def TIME_FONT(self):
        """  Returns the Time font.
        """
        return self.config["TIME"].get("font", "Curlz MT,36,-1,5,400,0,0,0,0,0,0,0,0,0,0,1,Regular")

    @TIME_FONT.setter
    def TIME_FONT(self, value):
        """  Sets the Time font.
        """
        self.config["TIME"]["font"] = value

    @property
    def TIME_ALIGNMENT(self):
        """  Returns the Time alignment.
        Aligns the text with the side of the screen - either Right, Left or None.
        """
        return self.config["TIME"].get("alignment", "Right")

    @TIME_ALIGNMENT.setter
    def TIME_ALIGNMENT(self, value):
        """  Sets the Time alignment.
             Aligns the text with the side of the screen - either Right, Left or None.
        """
        self.config["TIME"]["alignment"] = value

    @property
    def TIME_PREFIX(self):
        """  Returns the Time prefix character.
             Use to place a character at the start of the text time.
             Used if the font type can display a special glyph at the start of the text.
        """
        return self.config["TIME"].get("prefix", "")

    @TIME_PREFIX.setter
    def TIME_PREFIX(self, value):
        """  Sets the Time prefix character.
             Use to place a character at the start of the text time.
             Used if the font type can display a special glyph at the start of the text.
        """
        self.config["TIME"]["prefix"] = value

    @property
    def TIME_POSTFIX(self):
        """  Returns the Time postfix character.
             Use to place a character at the end of the text time.
             Used if the font type can display a special glyph at the end of the text.
        """
        return self.config["TIME"].get("postfix", "")

    @TIME_POSTFIX.setter
    def TIME_POSTFIX(self, value):
        """  Sets the Time prefix character.
             Use to place a character at the end of the text time.
             Used if the font type can display a special glyph at the end of the text.
        """
        self.config["TIME"]["postfix"] = value

    @property
    def TIME_SPACE(self):
        """  Returns the Time space character.
             Use to place a character in place of the space in text time.
             Used if the font type can display a special glyph instead of space.
        """
        return self.config["TIME"].get("space", "")

    @TIME_SPACE.setter
    def TIME_SPACE(self, value):
        """  Sets the Time space character.
             Use to place a character in place of the space in text time.
             Used if the font type can display a special glyph instead of space.
        """
        self.config["TIME"]["space"] = value

#---------------------------------------------------------------------------------------------- SOUNDS -----------------------
    @property
    def SOUNDS(self):
        """  Returns if sounds are enabled.
        """
        return self.config["SOUNDS"].get("sounds", True)

    @SOUNDS.setter
    def SOUNDS(self, value):
        """  Sets if sounds are enabled.
        """
        self.config["SOUNDS"]["sounds"] = value

    @property
    def SOUNDS_WESTMINSTER(self):
        """  Returns if sounds are enabled.
        """
        return self.config["SOUNDS"].get("westminster", True)

    @SOUNDS_WESTMINSTER.setter
    def SOUNDS_WESTMINSTER(self, value):
        """  Sets if sounds are enabled.
        """
        self.config["SOUNDS"]["westminster"] = value

    @property
    def SOUNDS_HOUR_CHIMES(self):
        """  Returns if hour chimes are enabled.
        """
        return self.config["SOUNDS"].get("hour_chimes", True)

    @SOUNDS_HOUR_CHIMES.setter
    def SOUNDS_HOUR_CHIMES(self, value):
        """  Sets if hour chimes are enabled.
        """
        self.config["SOUNDS"]["hour_chimes"] = value

    @property
    def SOUNDS_QUARTER_CHIMES(self):
        """  Returns if quarter chimes are enabled.
        """
        return self.config["SOUNDS"].get("quarter_chimes", True)

    @SOUNDS_QUARTER_CHIMES.setter
    def SOUNDS_QUARTER_CHIMES(self, value):
        """  Sets if quarter chimes are enabled.
        """
        self.config["SOUNDS"]["quarter_chimes"] = value

    @property
    def SOUNDS_HOUR_PIPS(self):
        """  Returns if hour pips are enabled.
        """
        return self.config["SOUNDS"].get("hour_pips", True)

    @SOUNDS_HOUR_PIPS.setter
    def SOUNDS_HOUR_PIPS(self, value):
        """  Sets if hour pips are enabled.
        """
        self.config["SOUNDS"]["hour_pips"] = value

    @property
    def SOUNDS_CUCKOO(self):
        """  Returns if sounds are enabled.
        """
        return self.config["SOUNDS"].get("cuckoo", True)

    @SOUNDS_CUCKOO.setter
    def SOUNDS_CUCKOO(self, value):
        """  Sets if sounds are enabled.
        """
        self.config["SOUNDS"]["cuckoo"] = value

    @property
    def SOUNDS_VOLUME(self):
        """  Returns if sound volume.
        """
        return self.config["SOUNDS"].get("sound_volume", True)

    @SOUNDS_VOLUME.setter
    def SOUNDS_VOLUME(self, value):
        """  Sets sound volume.
        """
        self.config["SOUNDS"]["sound_volume"] = value
#---------------------------------------------------------------------------------------------- EVENTS -----------------------
    @property
    def EVENTS_STAGE_1_DAYS(self):
        """  Returns the number of days due for stage 1.
        """
        return self.config["EVENTS"].get("stage1Days", 5)

    @EVENTS_STAGE_1_DAYS.setter
    def EVENTS_STAGE_1_DAYS(self, value):
        """  Sets the number of days due for stage 1.
        """
        self.config["EVENTS"]["stage1Days"] = value

    @property
    def EVENTS_STAGE_2_DAYS(self):
        """  Returns the number of days due for stage 2.
        """
        return self.config["EVENTS"].get("stage2Days", 10)

    @EVENTS_STAGE_2_DAYS.setter
    def EVENTS_STAGE_2_DAYS(self, value):
        """  Sets the number of days due for stage 2.
        """
        self.config["EVENTS"]["stage2Days"] = value

    @property
    def EVENTS_STAGE_3_DAYS(self):
        """  Returns the number of days due for stage 3.
        """
        return self.config["EVENTS"].get("stage3Days", 30)

    @EVENTS_STAGE_3_DAYS.setter
    def EVENTS_STAGE_3_DAYS(self, value):
        """  Sets the number of days due for stage 3.
        """
        self.config["EVENTS"]["stage3Days"] = value

    @property
    def EVENTS_STAGE_1_COLOUR(self):
        """  Returns the colour for stage 1.
        """
        return self.config["EVENTS"].get("stage1Colour", "red")

    @EVENTS_STAGE_1_COLOUR.setter
    def EVENTS_STAGE_1_COLOUR(self, value):
        """  Sets the the colour for stage 1.
        """
        self.config["EVENTS"]["stage1Colour"] = value

    @property
    def EVENTS_STAGE_2_COLOUR(self):
        """  Returns the colour for stage 2.
        """
        return self.config["EVENTS"].get("stage2Colour", "yellow")

    @EVENTS_STAGE_2_COLOUR.setter
    def EVENTS_STAGE_2_COLOUR(self, value):
        """  Sets the the colour for stage 2.
        """
        self.config["EVENTS"]["stage2Colour"] = value

    @property
    def EVENTS_STAGE_3_COLOUR(self):
        """  Returns the colour for stage 3.
        """
        return self.config["EVENTS"].get("stage3Colour", "green")

    @EVENTS_STAGE_3_COLOUR.setter
    def EVENTS_STAGE_3_COLOUR(self, value):
        """  Sets the the colour for stage 3.
        """
        self.config["EVENTS"]["stage3Colour"] = value

    @property
    def EVENTS_NOW_COLOUR(self):
        """  Returns the colour for events now due.
        """
        return self.config["EVENTS"].get("nowColour", "blue")

    @EVENTS_NOW_COLOUR.setter
    def EVENTS_NOW_COLOUR(self, value):
        """  Sets the colour for events now due.
        """
        self.config["EVENTS"]["nowColour"] = value



    def writeConfig(self):
        """ Write the current config file.
        """
        self.logger.debug("Writing configure file.")
        strNow  = datetime.datetime.now()
        written = strNow.strftime("%A %d %B %Y  %H:%M:%S")
        st_toml = toml.dumps(self.config)

        with open(self.FILE_NAME, "w") as configFile:       # In context manager.
            configFile.write("#   Configure file for pyKlock.py \n")
            configFile.write(f"#   (c) Kevin Scott   Written {written}\n")
            configFile.write("#\n")
            configFile.write("#   true and false are lower case \n")
            configFile.write("#\n")

            configFile.writelines(st_toml)


    def _writeDefaultConfig(self):
        """ Write a default configure file.
            This is hard coded  ** TO KEEP UPDATED **
        """
        strNow  = datetime.datetime.now()
        written = strNow.strftime("%A %d %B %Y  %H:%M:%S")
        config  = dict()

        config["INFO"] = {"myVERSION": "2026.38",
                          "myNAME"   : "pyKlock"}

        config["APPLICATION"] = {"x_pos"      : 100,
                                 "y_pos"      : 100,
                                 "width"      : 400,
                                 "height"     : 45,
                                 "confirmExit": False,
                                 "menu"       : True,
                                 "toolBar"    : True}

        config["DISPLAY"] = {"foreground" : "#00ff00",
                             "background" : "#000000",
                             "transparent": True,
                             "infoLine"   : True}

        config["TIME"] = {"mode"     : "Digital",
                          "format"   : "Fuzzy Time",
                          "font"     :  "Curlz MT,36,-1,5,400,0,0,0,0,0,0,0,0,0,0,1,Regular",
                          "alignment": "Right",
                          "prefix"   : "",
                          "postfix"  : "",
                          "space"    : " "}

        config["SOUNDS"] = {"sounds"        : True,
                            "westminster"   : True,
                            "hour_chimes"   : True,
                            "quarter_chimes": True,
                            "hour_pips"     : False,
                            "cuckoo"        : False,
                            "sound_volume"  : 25}

        config["EVENTS"] = {"stage1Days"   : 5,
                            "stage2Days"   : 10,
                            "stage3Days"   : 30,
                            "stage1Colour" : "red",
                            "stage2Colour" : "yellow",
                            "stage3Colour" : "green",
                            "nowColour"    : "blue"}

        st_toml = toml.dumps(config)

        with open(self.FILE_NAME, "w") as configFile:       # In context manager.
            configFile.write("#   DEFAULT Configure file for pyKlock.py \n")
            configFile.write(f"#   (c) Kevin Scott   Written {written}\n")
            configFile.write("#\n")
            configFile.write("#   true and false are lower case \n")
            configFile.write("\n")
            configFile.writelines(st_toml)                  # Write configure file.

        with open(self.FILE_NAME, "r") as configFile:       # In context manager.
            self.config = toml.load(configFile)             # Load the configure file, in toml.
