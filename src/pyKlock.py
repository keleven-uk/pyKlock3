###############################################################################################################
#    pyKlock3   Copyright (C) <2025>  <Kevin Scott>                                                           #                                                                                                             #    A klock built using QT framework.                              .                                         #
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

from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel, QLCDNumber, QVBoxLayout)
from PyQt6.QtCore import Qt, QTimer, QDateTime

import src.utils.klock_utils as utils             #  Need to install pywin32


class KlockWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("pyKlock")
        self.setGeometry(100, 100, 400, 200)

        # Create a central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("margin:0px; border:0px")
        self.setCentralWidget(central_widget)

        # Create a layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create an LCD Number display
        self.lcd = QLCDNumber()
        self.lcd.setDigitCount(8)  # Display 8 digits
        self.lcd.display("12:34:56")  # Show some initial value
        self.lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)  # Use filled segment style

        # Add LCD to the layout
        layout.addWidget(self.lcd)

        # Create a status bar
        self.status_bar = self.statusBar()

        self.stsDate   = QLabel("Thursday 23 October 2025")
        self.stsDate.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.stsState = QLabel("cisN")
        self.stsState.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stsIdle   = QLabel("idle : 7s")
        self.stsIdle.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.status_bar.addPermanentWidget(self.stsDate, 1)
        self.status_bar.addPermanentWidget(self.stsState, 1)
        self.status_bar.addPermanentWidget(self.stsIdle, 2)

        # Set up timer to update the clock
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)  # Update every second

        # Initialize with current time
        self.update_time()

    def update_time(self):
        current_time = QDateTime.currentDateTime()
        time_text = current_time.toString("hh:mm:ss")
        date_text = current_time.toString("dddd MMMM yyyy")
        self.lcd.display(time_text)
        self.stsDate.setText(date_text)
        self.stsState.setText(f"{utils.get_state()}")
        self.stsIdle.setText(utils.get_idle_duration())





