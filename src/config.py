###############################################################################################################
#    myConfig.py    Copyright (C) <2025>  <Kevin Scott>                                                       #
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
        return self.config["INFO"].get("myNAME", "pyDigitalKlock")

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

        config["INFO"] = {"myVERSION": "2025.3",
                          "myNAME"   : "pyKlock"}

        config["APPLICATION"] = {"x_pos" : 100,
                                 "y_pos" : 100,
                                 "width" : 400,
                                 "height": 200}

        config["DISPLAY"] = {"foreground": "#00ff00",
                             "background": "#000000"}


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
