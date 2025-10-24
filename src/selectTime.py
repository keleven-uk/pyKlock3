###############################################################################################################
#    selectTime.py   Copyright (C) <2017-25>  <Kevin Scott>                                                      #
#                                                                                                             #
#    A class which allows the current time to be displays in various formats.                                 #
#                                                                                                             #
#    If the module is run direct [not imported] a small tkinter program is loaded for testing purposes.       #
#                                                                                                             #
###############################################################################################################
#    Copyright (C) <2017-22>  <Kevin Scott>                                                                      #
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
import time
import math
#import logging

import src.utils.timeCodes as tc


class SelectTime:
    """   A class which allows the current time to be displays in various formats.
          The formats are held in the enum TimeTypes, these are exported.

          TimeType is set to the desired time format [from TimeTypes]
          getTime is then called and this will return the current time is the desired time format.
    """

    __types = ("Fuzzy Time", "Time in Words", "GMT Time", "Local Time", "UTC Time", "Swatch Time", "New Earth Time",
               "Julian Time", "Decimal Time", "True Hex Time", "Hex Time", "Oct Time", "Binary Time", "Roman Time",
               "Morse Time", "Mars Sol Date", "Coordinated Mars Time", "Flow Time", "Percent Time", "Metric Time",
               "Unix Time")
#
#  the class is access by the following properties only.
#  getTime can't be made a proper property, this seems to upset the dictionary of functions - they are not callable.

    @property
    def timeTypes(self):
        """ Returns a tuple of available Time types."""
        return self.__types

    def getTime(self, position=0):
        """ Returns a function to return the time at position in timeTypes."""
        return self.__funcs[position](self)

    #def __init__(self):
        #logging.basicConfig(filename='selectTime.log',
                            #filemode='w',
                            #format='%(name)s - %(levelname)s - %(message)s',
                            #level=logging.DEBUG)
        #logging.debug('init')


# -------------------------------------------------------------------------------- time functions ----------------------
#
# The time functions can't be made property's, this seems to upset the dictionary of functions - they are not callable.
#
    def __getNowTime(self):
        """  returns now as hour, munutes and seconds"""
        now = datetime.datetime.now()

        return now.hour, now.minute, now.second
# ------------------------------------------------------------------------------------- getGMTTime --------------------
    def getGMTTime(self):
        """ returns current time as GMT."""
        return time.strftime("%H:%M:%S", time.gmtime())

# ------------------------------------------------------------------------------------- getLocalTime -------------------
    def getLocalTime(self):
        """ returns current time as Local time."""
        return time.strftime("%H:%M:%S", time.localtime())

# ------------------------------------------------------------------------------------- getUTCTim ----------------------
    def getUTCTime(self):
        """ returns current time as UTC time."""
        return "{:%H:%M:%S}".format(datetime.datetime.utcnow())

# ------------------------------------------------------------------------------------- getFuzzyTime -------------------
    def getFuzzyTime(self):
        """ Returns current time as Fuzzy Time.
        """

        __hour, __mins, __secs = self.__getNowTime()
        __nrms = __mins - (__mins % 5)  # gets nearest five minutes
        __sRtn = ""

        __ampm = "in the morning" if __hour < 12 else "pm"

        if (__mins % 5) > 2:
            __nrms += 5  # closer to next five minutes, go to next

        __sRtn = tc.minsText[__nrms]  # look up text for minutes.

        if __nrms > 30:
            __hour += 1

        # generate output string according to the hour of the day.

        #   if the hour is 0 or 24 and no minutes - it must be midnight.
        #   if the hour is 12 and no minutes - it must be noon.

        #   if "pm" then afternoon, subtract 12 - only use 12 hour clock.

        if __hour == 12 and __sRtn == "":
            __fuzzyTime = "about Noon"
        elif __hour == 0 and __sRtn == "":
            __fuzzyTime = "about Midnight"
        elif __hour == 24 and __sRtn == "":
            __fuzzyTime = "about Midnight"
        else:
            if __ampm == "pm":
                __hour -= 12
                __ampm = "in the evening" if __hour > 5 else "in the afternoon"
            if __sRtn == "":
                __fuzzyTime = f" about {tc.hours[__hour]}'ish {__ampm}"
            else:
                __fuzzyTime = f" {__sRtn} {tc.hours[__hour]} {__ampm}"

        return __fuzzyTime

# ------------------------------------------------------------------------------------- getWordsTime -------------------
    def getWordsTime(self):
        """ Returns current time in words.
        """

        __hour, __mins, __secs = self.__getNowTime()
        __pasTo = "past"

        __ampm = "in the morning" if __hour < 12 else "pm"

        if __mins > 30:                                         # past the half hour - minutes to the hour.
            __hour += 1
            __pasTo = "to"
            __mins = 60 - __mins

        # generate output string according to the hour of the day.

        # if "pm" then afternoon, subtract 12 - only use 12 hour clock.

        if __ampm == "pm":
            __hour -= 12
            __ampm = "in the evening" if __hour >= 5 else "in the afternoon"

        if __mins == 0:
            __minsStr = f" {tc.hours[__hour]} o'clock {__ampm}"
        elif 1 <= __mins <= 9:
            __minsStr = f" {tc.units[__mins]} minutes {__pasTo} {tc.hours[__hour]} {__ampm}"
        elif 10 <= __mins <= 20:
            __minsStr = f" {tc.tens[__mins-9]} minutes {__pasTo} {tc.hours[__hour]} {__ampm}"
        elif 21 <= __mins <= 29:
            __minsTens = math.floor(__mins / 10)
            __minsUnit = __mins - (__minsTens * 10)
            __minsStr = f" twenty {tc.units[__minsUnit]} minutes {__pasTo} {tc.hours[__hour]} {__ampm}"
        else:
            __minsStr = f" thirty minutes past {tc.hours[__hour]} {__ampm}"

        return __minsStr

# ------------------------------------------------------------------------------------- getSwatchTime ------------------
    def getSwatchTime(self):
        """   returns UTC [+1 hour] time as Swatch Time.
              Swatch time is made up of 1000 beats per day i.e. 1 beat = 86.4 seconds.
              This is then encoded into a string.

              see http://en.wikipedia.org/wiki/Swatch_Internet_Time
        """

        __utcNow = datetime.datetime.utcnow()
        __utcPlus1 = __utcNow + datetime.timedelta(hours=+1)
        __noOfSeconds = (__utcPlus1.hour * 3600) + (__utcPlus1.minute * 60) + __utcPlus1.second
        __noOfBeats = __noOfSeconds / 86.4

        return f"@ {__noOfBeats:.2f} BMT"

# ------------------------------------------------------------------------------------- getNETTime ---------------------
    def getNETTime(self):
        """   Returns UTC time as New Earth Time.
              New Earth Time [or NET] splits the day into 360 degrees. each degree is
              further split into 60 minutes and further into 60 seconds.

              Only shows degrees and minutes - at the moment.

              see http://en.wikipedia.org/wiki/New_Earth_Time
        """

        __utcNow = datetime.datetime.utcnow()

        __hour = __utcNow.hour
        __mins = __utcNow.minute
        __secs = __utcNow.second

        __deg = __hour * 15 + (__mins // 4)
        __min = __mins - ((__mins // 4) * 4)
        __sec = math.floor((__secs + (__min * 60)) / 4)

        return f"{__deg} deg {__sec:02d} mins"

# ------------------------------------------------------------------------------------- getJulianTime ------------------
    def getJulianTime(self):
        """   returns UTC time as a Julian Date Time.
              Formulae pinched from http://en.wikipedia.org/wiki/Julian_day
        """

        now = datetime.datetime.utcnow()

        a = (14 - now.month) / 12
        y = now.year + 4800 - a
        m = now.month + (12 * a) - 3

        jt = now.day + ((153 * m + 2) / 5) + (365 * y) + (y / 4) + (y / 100) - 32045
        jt = jt + ((now.hour - 12) / 24) + (now.minute / 1440) + (now.second / 86400)

        return f"{jt:.5f}"

# ------------------------------------------------------------------------------------- getDecimalTime -----------------
    def getDecimalTime(self):
        """   Returns the current [local] time in decimal notation.
              The day is divided into 10 hours, each hour is then split into 100 minutes of 100 seconds.

              see http://en.wikipedia.org/wiki/Decimal_time

              NB : :02d formats the number to be 2 digits with a leading zero if necessary.
        """

        __hour, __mins, __secs = self.__getNowTime()

        __noOfSeconds = (__hour * 3600) + (__mins * 60) + __secs
        __noOfDecimalSeconds = __noOfSeconds / 0.864

        __hour = math.floor(__noOfDecimalSeconds / 10000)
        __mins = math.floor((__noOfDecimalSeconds - (__hour * 10000)) / 100)
        __secs = math.floor(__noOfDecimalSeconds - (__hour * 10000) - (__mins * 100))

        return f"{__hour:02d}h {__mins:02d}m {__secs:02d}s"

# ------------------------------------------------------------------------------------- getTrueHexTime -----------------
    def getTrueHexTime(self):
        """   Returns the current [local] time in Hexadecimal time.
              The day is divided in 10 (sixteen) hexadecimal hours, each hour in 100 (two hundred and fifty-six)
              hexadecimal minutes and each minute in 10 (sixteen) hexadecimal seconds.

              see http://en.wikipedia.org/wiki/Hexadecimal_time

              NB : :02X formats the number to be 2 digits with a leading zero if necessary - but in hexadecimal.
        """

        __hour, __mins, __secs = self.__getNowTime()

        __noOfSeconds = (__hour * 3600) + (__mins * 60) + __secs
        __noOfHexSeconds = math.floor(__noOfSeconds * (65536 / 84600))

        __hour = math.floor(__noOfHexSeconds / 4096)
        __mins = math.floor((__noOfHexSeconds - (__hour * 4096)) / 16)
        __secs = __noOfHexSeconds % 16

        return f"{__hour:02X}_{__mins:02X}_{__secs:02X}"

# ------------------------------------------------------------------------------------- getHexTime ---------------------
    def getHexTime(self):
        """   Returns current [local] time in hex [base 16] format.
              This is only a hex representation of the current time
        """

        __hour, __mins, __secs = self.__getNowTime()

        return f"{__hour:02X}_{__mins:02X}_{__secs:02X}"

# ------------------------------------------------------------------------------------- getOctTime ---------------------
    def getOctTime(self):
        """   Returns current [local] time in oct [base 8] format.
              This is only a hex representation of the current time

              NB : :02o formats the number to be 2 digits with a leading zero if necessary - but in octal.
        """

        __hour, __mins, __secs = self.__getNowTime()

        return f"{__hour:02o}_{__mins:02o}_{__secs:02o}"

# ------------------------------------------------------------------------------------- getBinTime ---------------------
    def getBinTime(self):
        """   Returns current [local] time in Binary [base 2] format.
              This is only a hex representation of the current time

              NB : :06b formats the number to be 6 digits with a leading zero if necessary - but in binary.
                        Only need to use 6 binary digits to hold numbers up to 60.
                        Also, could of used bin(__hours); but output is 0b10011
        """

        __hour, __mins, __secs = self.__getNowTime()

        return f"{__hour:06b}_{__mins:06b}_{__secs:06b}"

# ------------------------------------------------------------------------------------- getRomanTime -------------------
    def getRomanTime(self):
        """   Returns the current [local] time in Roman numerals.
        """

        __hour, __mins, __secs = self.__getNowTime()

        __Rhour = tc.romanNumerals[__hour]
        __Rmins = tc.romanNumerals[__mins]
        __Rsecs = tc.romanNumerals[__secs]

        return f"{__Rhour}:{__Rmins}:{__Rsecs}"

# ------------------------------------------------------------------------------------- getMorseTime -------------------
    def getMorseTime(self):
        """   Returns the current [local] time with each digit represented by a Morse code.
        """

        __hour, __mins, __secs = self.__getNowTime()

        if __hour < 10:
            __Mhour = "{0} {1}".format(tc.morseCode[0], tc.morseCode[__hour])
        else:
            __Mhour = "{0} {1}".format(tc.morseCode[int(__hour/10)], tc.morseCode[__hour % 10])

        if __mins < 10:
            __Mmins = "{0} {1}".format(tc.morseCode[0], tc.morseCode[__mins])
        else:
            __Mmins = "{0} {1}".format(tc.morseCode[int(__mins/10)], tc.morseCode[__mins % 10])

        if __secs < 10:
            __Msecs = "{0} {1}".format(tc.morseCode[0], tc.morseCode[__secs])
        else:
            __Msecs = "{0} {1}".format(tc.morseCode[int(__secs/10)], tc.morseCode[__secs % 10])

        return f"{__Mhour}:{__Mmins}:{__Msecs}"

# ------------------------------------------------------------------------------------- getMarsSolDate------------------
    def getMarsSolDate(self):
        """   Returns the current [UTC] time as Mars Sol Date.

              see http://jtauber.github.io/mars-clock/
        """

        __SolDataEpoch = datetime.datetime(day=6, month=1, year=2000)
        __utcNow = datetime.datetime.utcnow()
        __daysSinceEpoch = (__utcNow - __SolDataEpoch).days + (__utcNow - __SolDataEpoch).seconds / 86400
        __MarsSolDate = (__daysSinceEpoch / 1.027491252) + 44796.0 - 0.00096

        return f"{__MarsSolDate:5.5f}"

# ------------------------------------------------------------------------------------- getCoordinatedMarsTime ---------
    def getCoordinatedMarsTime(self):
        """   Returns the current [UTC] time as Coordinated Mars Time.

              see http://jtauber.github.io/mars-clock/
        """

        __SolDataEpoch = datetime.datetime(day=6, month=1, year=2000)
        __utcNow = datetime.datetime.utcnow()
        __daysSinceEpoch = (__utcNow - __SolDataEpoch).days + (__utcNow - __SolDataEpoch).seconds / 86400

        __marsSolDate = (__daysSinceEpoch / 1.027491252) + 44796.0 - 0.00096

        __mtc = (24 * __marsSolDate) % 24

        __hour = int(__mtc)
        __mins = (__mtc - __hour) * 60
        __secs = (__mins - int(__mins)) * 60

        return f"{__hour:02.0f}:{__mins:02.0f}:{__secs:02.0f}"

# ------------------------------------------------------------------------------------- getFlowTime -------------------
    def getFlowTime(self):
        """   Returns the current [local] time as Flow Time.
              Flow Time still divides the day into 24 hours, but each hour is divided into 100 minutes of 100 seconds.
              A Quick conversion is takes 2/3 of the minute [or second] and add it to it's self.
        """

        __hour, __mins, __secs = self.__getNowTime()
        __mins *= (5/3)
        __secs *= (5/3)

        return f"{__hour:02.0f}:{__mins:02.0f}:{__secs:02.0f}"

# ------------------------------------------------------------------------------------- getPercentTime -----------------
    def getPercentTime(self):
        """   Returns the current [local] time as a percent of the day.
              See http://raywinstead.com/metricclock.shtml
        """

        __hour, __mins, __secs = self.__getNowTime()

        __noOfSeconds = (__hour * 3600) + (__mins * 60) + __secs
        __percentSeconds = __noOfSeconds / 86400 * 100

        return f"{__percentSeconds:02.4f} PMH"

# ------------------------------------------------------------------------------------- getMetricTime ------------------
    def getMetricTime(self):
        """   Returns the current [local] time in Metric time.
              Metric time is the measure of time interval using the metric system, which defines the second as the base unit of time,
              and multiple and submultiple units formed with metric prefixes, such as kiloseconds and milliseconds.
              Only Kiloseconds are used here.
        """

        __hour, __mins, __secs = self.__getNowTime()

        __noOfSeconds = ((__hour * 3600) + (__mins * 60) + __secs) / 1000

        return f"{__noOfSeconds} Kiloseconds"

# ------------------------------------------------------------------------------------- getUnixTime --------------------
    def getUnixTime(self):
        """   Returns UTC in Unix time.
        Unix time, or POSIX time, is a system for describing instants in time, defined as the number of seconds
        elapsed since midnight Coordinated Universal Time (UTC) of Thursday, January 1, 1970  """

        __tday = datetime.datetime.utcnow()
        __epoch = datetime.datetime(1970, 1, 1)
        __secs = (__tday - __epoch).total_seconds()

        return f"{__secs:.0f}"

    #
    # GLOBAL Dictionary that holds references to all the time functions.
    __funcs = {"Fuzzy Time": getFuzzyTime,
               "Time in Words": getWordsTime,
               "GMT Time": getGMTTime,
               "Local Time": getLocalTime,
               "UTC Time": getUTCTime,
               "Swatch Time": getSwatchTime,
               "New Earth Time": getNETTime,
               "Julian Time": getJulianTime,
               "Decimal Time": getDecimalTime,
               "True Hex Time": getTrueHexTime,
               "Hex Time": getHexTime,
               "Oct Time": getOctTime,
               "Binary Time": getBinTime,
               "Roman Time": getRomanTime,
               "Morse Time": getMorseTime,
               "Mars Sol Date": getMarsSolDate,
               "Coordinated Mars Time": getCoordinatedMarsTime,
               "Flow Time": getFlowTime,
               "Percent Time": getPercentTime,
               "Metric Time": getMetricTime,
               "Unix Time": getUnixTime}


#
# ----------------------------------------------------- called to test, if run as main (not imported) ------------------
#
if __name__ == "__main__":
    import tkinter as tk
    import tkinter.ttk as ttk
    import win32com.client

    def update_agent(text):
        """  Display the agent and speak the text [time].
        """
        name = "dog"

        agent=win32com.client.Dispatch("Agent.Control.2")
        agent.Connected=True
        agent.Characters.Load(name, name + ".acs")

        char = agent.Characters(name)

        char.LanguageID = 0x409
        char.Show()
        char.Play("Greet")
        char.Speak(text)
        char.Hide()

        while char.visible:
            pass

        agent.Connected=False
        agent.Characters.Unload(name)


    def update_timeText():
        # Get the current time

        current = s.getTime(position=timeCombo.get())

        if update_timeText.old_current != current:
            update_timeText.old_current = current  #  Static variable of update_timeText, so it will persists between function calls
            #update_agent(current)

            # Update the timeText label box with flexi time.
            timeText.configure(text=current)

            root.wm_title("SelectTime Test :: " + time.strftime("%H:%M:%S", time.localtime()))

        # Call the update_timeText() function every 1 second.
        root.after(1000, update_timeText)

    update_timeText.old_current = ""  #  Static variable of update_timeText, so it will persists between function calls
    s = SelectTime()

    root = tk.Tk()
    root.wm_title("SelectTime Test")

    # create a combobox
    timevar = tk.StringVar()
    timeCombo = ttk.Combobox(root, textvariable=timevar, values=list(s.timeTypes))
    timeCombo.current(0)
    timeCombo.pack()

    # create a timeText label (a text box)
    timeText = ttk.Label(root, text="", font=("Helvetica", 20))
    timeText.pack()

    update_timeText()
    root.mainloop()
