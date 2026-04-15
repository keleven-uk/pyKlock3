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

from PyQt6.QtCore import QObject, pyqtSignal, QTimer

class countdown(QObject):
    """  A Simple class that implements a countdown timer.
         The class is self contained - with an internal timer.

        The class uses PyQt signals and slots to communicate with the outside world.

        A countDownTick is emitted every second the cound down timer is running.
            Call self.countDown.elapsedTime to read the elapsed time.
        
        A countDownEnd is emitted when the count down timer has counted down the desired interval.

         Usage:
            self.countDown = cd.countdown(self)
            self.countDown.countDownTick.connect(self.updateTime)                 #  Signal is fired when the count down is running, update display.
            self.countDown.countDownEnd.connect(self.endEvent)                    #  Signal is fired when the count down has ended.

            self.countDown.start(target)                                          #  Starts the count down timer with a supplied time interval in minutes.
            self.countDown.reset()                                                #  Called to reset the object, so a second count down can be called.
    """

    countDownEnd  = pyqtSignal()  # <-- This is the sub window's signal
    countDownTick = pyqtSignal()  # <-- This is the sub window's signal

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.reset()                            #  Sets up object’s attributes.

        #  Set up short timer to update the clock every second
        #  Will be destroyed when the calling window is closed.
        self.Timer = QTimer(self)               
        self.Timer.timeout.connect(self.tick)
        
    def reset(self):
        """  Creates the object’s attributes.

             Called to reset the object, so a second count down can be called.
        """
        self.is_running = False
        self.target     = 0

    def start(self, target_time):
        """  Start the countdown timer, which will count down until target_time is zero.
             The target time is passed in minutes and converted to seconds.
        """
        self.is_running = True
        self.target     = target_time
        self.Timer.start(1000)

    @property
    def countdownRunning(self):
        return self.is_running

    def tick(self):
        if self.target == 0:
            self.countDownEnd.emit()      #  emit signal when count down ends.
            self.is_running = False
            self.Timer.stop()
        else:
            self.countDownTick.emit()     #  emit signal if count down is running.
            self.target -= 1

    @property
    def elapsedTime(self):
        """  Returns the current value in hours, minutes seconds {00:00:00}

             If the countdown is not running "00:00:00" is returned.
        """
        if not self.is_running:
            return "00:00:00"

        minutes, seconds = divmod(self.target, 60)
        hours, minutes   = divmod(minutes, 60)

        trg = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return trg

    def clear(self):
        self.is_running = False
        self.Timer.stop()
        self.reset()                #  Sets up object’s attributes.
