###############################################################################################################
#     stopwatch.py   Copyright (C) <2022>  <Kevin Scott>                                                      #                                                                                                             #                                                                                                             #
#     A simple class that implements a stopwatch.                                                             #
#                                                                                                             #
#     For changes see history.txt                                                                             #
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

class timer():
    """  A Simple class that implements a stopwatch.

         The stopwatch currently only ticks once every second.

    usage:
        stopwatch = timer()
        stopwatch.start()           Starts the stopwatch.
        stopwatch.stop()            Stops the stopwatch, stops the ticks.
        stopwatch.pause()           Pauses the stopwatch, the ticks still continue.
        stopwatch.elapsed_time      Return the current value of the stopwatch.
        stopwatch.timer_running     Returns True if the stopwatch has been started.
    """

    def __init__(self):
        self.is_running   = False
        self.start_time   = 0
        self.time_elapsed = 0

    def start(self):
        self.is_running = True
        self.start_time = time.time()

    def stop(self):
        self.is_running = False

    def clear(self):
        self.is_running = False
        self.start_time = 0

    def pause(self):
        self.is_running = False
        self.pauseTime = time.time()

    def resume(self):
        self.is_running = True

    @property
    def timer_running(self):
        return self.is_running

    @property
    def elapsed_time(self):
            """  Returns the current value [ticks] in hours, minutes seconds {00:00:00}
                The stopwatch currently only ticks once every second.

                id the stopwatch is paused return the paused time.

                If the stopwatch is not running "00:00:00" is returned.
            """
            if self.timer_running:
                time_elapsed     = int(time.time() - self.start_time)
                minutes, seconds = divmod(time_elapsed, 60)
                hours, minutes   = divmod(minutes, 60)

                elps = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                return elps
            if self.start_time == 0:
                return "00:00:00"
            else:
                time_elapsed     = int(self.pauseTime - self.start_time)
                minutes, seconds = divmod(time_elapsed, 60)
                hours, minutes   = divmod(minutes, 60)

                elps = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                return elps
