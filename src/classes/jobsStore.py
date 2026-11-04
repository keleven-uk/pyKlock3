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

import csv

import src.projectPaths as pp


class jobsStore():
    """  A class that implements a store for jobs.
         The store is implemented as a dictionary - [key, item].
         The key is a string - Job Name.
         The item is a list  - Name, Time Period, job.
    """
# ------------------------------------------------------------------------------------- __init__ ----------------------
    def __init__(self, parent, myLogger, myConfig):
        self.parent     = parent
        self.myConfig   = myConfig
        self.myLogger   = myLogger
        self.store      = {}         #  Create the store, an empty dictionary.
        self.Headers    = ["Job Name", "Time Period", "Job"]
        self.Categories = ["", "Check Server"]
        self.storeName  = pp.JB_DATA_PATH

        self.loadJobs()

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
# ------------------------------------------------------------------------------------- getEvents ---------------------
    def getJobs(self):
        """  Retrieves jobs in list format.
        """
        lstJobs = []
        for key in sorted(self.store):
            lstJobs.append(self.store[key]) 

        return lstJobs
# ------------------------------------------------------------------------------------- saveEvents --------------------
    def saveJobs(self):
        """  Saves the jobs store to a text file in csv format.
        """
        with open (self.storeName, "w", newline="", encoding="utf-8") as csvFile:
            writer = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
            for key in sorted(self.store):
                print(self.store[key])
                writer.writerow(self.store[key])
# ------------------------------------------------------------------------------------- loadEvents --------------------
    def loadJobs(self):
        """  Loads the jobs store from a text file in csv format.
        """
        try:
            with open (self.storeName, "r", encoding="utf-8") as csvFile:
                csvFile = csv.reader(csvFile)
                for row in csvFile:
                    key = f"{row[0]}"
                    print(row)
                    self.store[key] = row

        except FileNotFoundError:
            self.myLogger.info(" File not found, will use an empty Jobs store.")







