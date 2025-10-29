###############################################################################################################
#    projectPaths.py   Copyright (C) <2025>  <Kevin Scott>                                                    #                                                                                                             #                                                                                                             #
#    Holds common directory paths for the project.                                                            #
#        Must sit in src directory                                                                            #
#                                                                                                             #
#     For changes see history.txt                                                                             #
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

"""  A place to hold all the common project paths.
     Also, holds some common constants used in the project.
"""
import sys
import pathlib

PROJECT_PATH  = pathlib.Path(__file__).parent
MAIN_PATH     = pathlib.Path(__file__).parent.parent

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):   #  Running as a stand alone executable.
    CONFIG_PATH   = "config.toml"
    LOGGER_PATH   = "pyKlock.log"
    RESOURCE_PATH = "resources"
else:
     CONFIG_PATH   = MAIN_PATH / "config.toml"
     LOGGER_PATH   = MAIN_PATH / "logs/pyKlock.log"
     RESOURCE_PATH = MAIN_PATH / "resources"

