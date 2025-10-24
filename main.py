###############################################################################################################
#    pyKlock3   Copyright (C) <2025>  <Kevin Scott>                                                           #
#                                                                                                             #
#    The Klock displays the time [local], date, key status  and the computers idle time.                      #
#       Key status is the status of Caps Lock, Scroll lock and Num lock.                                      #
#                                                                                                             #
#    To install dependencies pip install -r requirements.txt                                                  #
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

import sys
import platform

from PyQt6.QtWidgets import (QApplication)

import src.pyKlock as pyKlock
import src.config as Config
import src.logger as Logger

from src.projectPaths import LOGGER_PATH, CONFIG_PATH

############################################################################################### __main__ ######

if __name__ == "__main__":

    my_logger  = Logger.get_logger(str(LOGGER_PATH))    # Create the logger.

    my_logger.info("-" * 100)

    my_config  = Config.Config(CONFIG_PATH, my_logger)  # Create the config.

    my_logger.info(f"  Running {my_config.NAME} Version {my_config.VERSION} ")
    my_logger.debug(f" {platform.uname()}")
    my_logger.debug(f" Python Version {platform.python_version()}")
    my_logger.debug("")

    my_logger.info(f"  Config path {CONFIG_PATH}")
    my_logger.info(f"  Logger path {LOGGER_PATH}")

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = pyKlock.KlockWindow()
    window.show()
    sys.exit(app.exec())

    my_logger.info(f"  Ending {my_config.NAME} Version {my_config.VERSION} ")
    my_logger.info("=" * 100)
