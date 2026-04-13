###############################################################################################################
#     countdown.py   Copyright (C) <2026>  <Kevin Scott>                                                      #                                                                                                             #                                                                                                             #
#     A simple class that implements a countdown timer.                                                       #
#                                                                                                             #
#     For changes see history.txt                                                                             #
#                                                                                                             #
###############################################################################################################
#    Copyright (C) <2026>  <Kevin Scott>                                                                      #
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

from pyqttoast import Toast, ToastPreset

class countdown():
    """  A Simple class that implements a countdown timer.

         Usage:
            myCountdown = countdown(window)
            myCountdown.start(n)               #  Starts the countdown of n minutes.)
            myCountdown.elapsedTime()          #  Decrements the countdown, should be called regularly [i.e. every second].
            myCountdown.clear                  #  Cancels the current countdown and sets everything back to the start.
    """
    def __init__(self, parent):
        self.parent     = parent
        self.is_running = False
        self.target     = 0

    def start(self, target_time):
        """  Start the countdown timer, which will count down until target_time is zero.
             The target time is passed in minutes and converted to seconds.
        """
        self.is_running = True
        self.target     = target_time * 60

    @property
    def countdownRunning(self):
        return self.is_running

    @property
    def elapsedTime(self):
        """  Returns the current value in hours, minutes seconds {00:00:00}

             If the countdown is not running "00:00:00" is returned.
        """

        if self.target == 0:
            self.is_running = False
            self.endStuff()
            return "00:00:00"
        else:
            self.target -= 1

        minutes, seconds = divmod(self.target, 60)
        hours, minutes   = divmod(minutes, 60)

        trg = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return trg

    def clear(self):
        self.is_running = False

    def endStuff(self):
        toast = Toast(self.parent)
        toast.setDuration(0)        #  Do not timeout.
        toast.applyPreset(ToastPreset.INFORMATION_DARK)
        toast.setTitle("Count Down Timer")
        toast.setText("Count Down Timer Finished.")
        toast.show()