###############################################################################################################
#     stopwatch.py   Copyright (C) <2022-26>  <Kevin Scott>                                                   #
#     A simple class that implements a stopwatch.                                                             #
#                                                                                                             #
#     For changes see history.txt                                                                             #
#                                                                                                             #
#     March 2026    Changed the timer to use timer.perf_Counter()                                             #
#                                                                                                             #
###############################################################################################################
#    Copyright (C) <2022>  <Kevin Scott>                                                                      #
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

import time

from datetime import timedelta

class timer():
    """  A Simple class that implements a stopwatch.

    usage:
        stopwatch = timer()
        stopwatch.start()           Starts the stopwatch.
        stopwatch.stop()            Stops the stopwatch, stops the ticks.
        stopwatch.pause()           Pauses the stopwatch, the ticks still continue.
        stopwatch.elapsedTime       Return the current value of the stopwatch.
        stopwatch.timerRunning      Returns True if the stopwatch has been started.
    """

    def __init__(self):
        self.isRunning= False
        self.startTime   = 0

    def start(self):
        self.isRunning= True
        self.startTime  = time.perf_counter()

    def stop(self):
        self.isRunning= False

    def clear(self):
        self.isRunning= False
        self.start_time = 0
        self.duration = "00:00:00.000000"

    def pause(self):
        self.isRunning= False

    def resume(self):
        self.isRunning= True

    @property
    def timerRunning(self):
        return self.isRunning

    @property
    def elapsedTime(self):
            """  Returns the current value [ticks] in hours, minutes seconds {00:00:00}

                If the stopwatch is paused return the paused time.

                If the stopwatch is not running "00:00:00.00" is returned.
                    The [-4] is used to truncate to 2 decimal places.
            """
            if self.timerRunning:
                self.duration = str(timedelta(seconds=time.perf_counter()- self.startTime))
                return self.duration[:-4]
            if self.startTime == 0:
                return "00:00:00.00"
            else:
                return self.duration[:-4]
