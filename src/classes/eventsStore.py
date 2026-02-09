###############################################################################################################
#    eventsStore.py   Copyright (C) <2024-26>  <Kevin Scott>                                                  #
#    For changes see history.txt                                                                              #
#                                                                                                             #
#    A store class for the saving and manipulation of events.                                                 #
#                                                                                                             #
#    An event is a named object that consists data and a due date and/or due time.                            #
#                                                                                                             #
#    an event -  a data item of each item in Headers, defined below.                                          #
#                                                                                                             #
#    import src.classes.eventsStore as es                                                                     #
#                                                                                                             #
#    eventsStore     = es.eventsStore()                                                                       #
#                                                                                                             #
#    eventsStore.getHeaders           Retrieves the headers for display, as strings.                          #
#    eventsStore.getCategories        Retrieves the categories for display, as strings.                       #
#    eventsStore.addEvent(key, item)  Adds an event to the store.  Key = name, item = all data.               #
#    eventsStore.getEvent(rowKey)     Retrieves an event matching name.                                       #
#    eventsStore.getEvents()          Returns all events as a sorted list.                                    #
#    eventsStore.saveFriends()        Saves the event store to disc in CSV format.                            #
#                                                                                                             #
#    The class should load the CSF file on start up, if not an empty sore is created.                         #
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
import csv

import src.projectPaths as pp
from pyqttoast import Toast, ToastPreset, ToastIcon, ToastPosition, ToastButtonAlignment


class eventsStore():
    """  A class that implements a store for friends.
         The store is implemented as a dictionary - [key, item].
         The key is a string - Event Name.
         The item is a list  - Name, Date Due, Time, Due, Category, Notes, Time Left, Stage 1, stage 2, stage 3, NOW.
    """
# ------------------------------------------------------------------------------------- __init__ ----------------------
    def __init__(self, parent, myLogger, myConfig):
        self.parent     = parent
        self.myConfig   = myConfig
        self.myLogger   = myLogger
        self.store      = {}         #  Create the store, an empty dictionary.
        self.Headers    = ["Event Name", "Date Due", "Time Due", "Category", "Recurring", "Notes", "Left"]
        self.Categories = ["", "Birthday", "Wedding Anniversary", "Anniversary", "Moto", "Holiday", "Appointment", "One Off Event", "Other"]
        self.storeName  = pp.EV_DATA_PATH

        self.loadEvents()

        self.stage1 = self.myConfig.EVENTS_STAGE_1_DAYS  * 86400    #   5 days in seconds, is really soon
        self.stage2 = self.myConfig.EVENTS_STAGE_2_DAYS * 86400     #  10 days in seconds, Will very soon be here
        self.stage3 = self.myConfig.EVENTS_STAGE_3_DAYS * 86400     #  30 days in seconds, will soon be here

        self.stage1Colour = self.myConfig.EVENTS_STAGE_1_COLOUR
        self.stage2Colour = self.myConfig.EVENTS_STAGE_2_COLOUR
        self.stage3Colour = self.myConfig.EVENTS_STAGE_3_COLOUR
        self.nowColour    = self.myConfig.EVENTS_NOW_COLOUR
# ------------------------------------------------------------------------------------- getHeaders --------------------
    @property
    def getHeaders(self):
        """  Returns a list of accepted event Headers i.e. Name, Date Due, Time Due etc.
        """
        return self.Headers
# ------------------------------------------------------------------------------------- getCategories -----------------
    @property
    def getCategories(self):
        """  Returns a list of accepted event Categories i.e. Birthday, Anniversary, Moto etc.
        """
        return self.Categories
# ------------------------------------------------------------------------------------- addEvent ----------------------
    def addEvent(self, key, item):
        """   Stores event data into the store.
        """
        self.store[key] = item
# ------------------------------------------------------------------------------------- deleteEvent -------------------
    def deleteEvent(self, key):
        """   Deletes a event from the store if it exist, if not ignore.
              If deleted, save the events store.
        """
        if key in self.store:
            del self.store[key]
            self.saveEvents()
# ------------------------------------------------------------------------------------- numberOfEvents ----------------
    @property
    def numberOfEvents(self):
        """  Returns the number of events in the store.
        """
        return len(self.store)
# ------------------------------------------------------------------------------------- getEvent ----------------------
    def getEvent(self, key):
        """  Retrieves a single event in list format.
             If the key doesn't exist, return error massage in the Notes filed.'
        """
        try:
            return self.store[key]
        except KeyError:
            return ["", "", "", "", "", "Record not found", ""]             #  May need to extend for extra fields,
                                                                             #  so the error message is always in the notes field.
# ------------------------------------------------------------------------------------- getEvents ---------------------
    def getEvents(self):
        """  Retrieves events in list format.
        """
        lstEvent = []
        for key in sorted(self.store):
            lstEvent.append(self.store[key][0:7])                           #  Don't return stage flags.'

        return lstEvent
# ------------------------------------------------------------------------------------- updateEvents ------------------
    def updateEvents(self):
        """  For each event in the store, calculate the time between the due date and now.
             The time interval, in seconds, is stored to the end of the event data,
             to be investigated later.
        """
        now = datetime.datetime.now()
        for key in self.store.copy():
            dateDue = self.store[key][1]
            dateDue = self.checkYear(dateDue, now)
            timeDue = self.store[key][2]
            dtDue   = datetime.datetime.strptime(f"{dateDue} {timeDue}", "%d/%m/%Y %H:%M")  #  Now a dateTime
            dtLeft  = int((dtDue - now).total_seconds())                                    #  Convert timedelta to seconds.

            self.store[key][6] = self.__formatSeconds(dtLeft)      #  Time left in seconds.
            self.__checkEvent(key, dtLeft)
# ------------------------------------------------------------------------------------- checkYear ---------------------
    def checkYear(self, dateDue, now):
        """  Rule 1 : If the year if before the current year [i.e. original birthday year] use current year.
             Rule 2 : If the month is before the current month [i.e. original birthday month] add 1 to year.
             Rule 3 : If the day is before the current day [i.e. original birthday day] add 1 to year.

             for example - if now if 27/11/2024 and date due is 02/04/1958.
                           Should return 02/04/2025.

             Both dateDue input and output are in string format.
             now is input in datetime format.

              Made the method callable, is a means of determining the actual due date.
        """
        curDay   = now.day
        curMonth = now.month
        curYear  = now.year
        dueDate  = datetime.datetime.strptime(dateDue, "%d %B %Y")  #  Convert string to Python dateTime.
        dueDay   = dueDate.day
        dueMonth = dueDate.month
        dueYear  = dueDate.year

        if dueYear < curYear:
            dueYear = curYear
        if dueMonth < curMonth:
            dueYear = curYear + 1
        if dueYear == curYear and dueMonth == curMonth and dueDay < curDay:  #  Event has just passed this month.
            dueYear = curYear + 1

        return f"{dueDay}/{dueMonth}/{dueYear}"
# ------------------------------------------------------------------------------------- _checkEvent -------------------
    def __checkEvent(self, key, secondsLeft):
        """  For each event, calculate the time left in seconds.
             Store that on the event, formatted into days, minutes and seconds for display.
             If the time left falls into the stages the process event.

                Stage 3 becomes active after 30 days.
                Stage 2 becomes active after 10 days.
                stage 1 becomes active after 1 day.
                Now becomes active with 1 minute to go - mainly intended for event with a time.
        """
        match secondsLeft:
            case secondsLeft if (secondsLeft <= 60 and self.store[key][10] == "False"):
                print("Now")
                self.__eventDue(key, "Now")
            case secondsLeft if (secondsLeft <= self.stage3 and self.store[key][9] == "False"):
                self.__eventDue(key, "Stage 3")
            case secondsLeft if (secondsLeft <= self.stage2 and self.store[key][8] == "False"):
                self.__eventDue(key, "Stage 2")
            case secondsLeft if (secondsLeft <= self.stage1 and self.store[key][7] == "False"):
                self.__eventDue(key, "Stage 1")
# ------------------------------------------------------------------------------------- _eventDue ---------------------
    def __eventDue(self, key, stage):
        """  Called when an event is found to be due.
             An appropriate notification is displayed for the event.
        """
        event     = self.store[key]
        eventDue  = event[6]
        eventName = event[0]
        toast = Toast(self.parent)
        toast.setDuration(0)        #  Do not timeout.
        toast.applyPreset(ToastPreset.INFORMATION_DARK)
        toast.setTitle("Event Reminder")
        toast.setText(f" {eventName} in {eventDue}")

        match stage:
            case "Stage 3":
                self.store[key][9] = "True"

            case "Stage 2":
                self.store[key][8] = "True"

            case "Stage 1":
                self.store[key][7] = "True"

            case "Now":
                self.store[key][10] = "True"
                toast.setText(f" {eventName}  NOW")
        
        toast.show()
        self.saveEvents()
# ------------------------------------------------------------------------------------- saveEvents --------------------
    def saveEvents(self):
        """  Saves the event store to a text file in csv format.
        """
        with open (self.storeName, "w", newline="", encoding="utf-8") as csvFile:
            writer = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
            for key in sorted(self.store):
                writer.writerow(self.store[key])
# ------------------------------------------------------------------------------------- loadEvents --------------------
    def loadEvents(self):
        """  Loads the event store from a text file in csv format.
        """
        try:
            with open (self.storeName, "r", encoding="utf-8") as csvFile:
                csvFile = csv.reader(csvFile)
                for rows in csvFile:
                    key = f"{rows[0]}"
                    item = rows
                    self.store[key] = item

        except FileNotFoundError:
            print("Event store not found, using empty sore.")
# ------------------------------------------------------------------------------------- _formatSeconds ----------------
    def __formatSeconds(self, seconds):
        """  Formats number of seconds into a human readable form i.e. hours:minutes:seconds

            Based from klock_utils.py, to make the class self accessing.
        """
        (days, remainder)  = divmod(seconds, 86400)
        (hours, remainder) = divmod(remainder, 3600)
        (minutes, seconds) = divmod(remainder, 60)

        if days:
            return f"{days:.0f}d {hours:.0f}h:{minutes:.0f}m"
        elif hours:
            return f"{hours:.0f}h {minutes:.0f}m"
        else:
            return f"{minutes:.0f}m"






