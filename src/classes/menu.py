###############################################################################################################
#    menu   Copyright (C) <2025-26>  <Kevin Scott>                                                            #
#                                                                                                             #
#    Constructs the main menu.                                                                                #
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

from PyQt6.QtWidgets import QMenuBar, QToolBar, QMenu, QComboBox
from PyQt6.QtGui     import QAction, QIcon
from PyQt6.QtCore    import QSize

import src.classes.styles as styles
import src.classes.selectTime as st

import src.windows.friendsViewer as fv
import src.windows.eventsViewer as ev

from src.projectPaths import RESOURCE_PATH

class Menu(QMenuBar):
    """  Constructs the main menu.

         self.myMenu.setVisible(self.menu_bar)  -  Creates the menu object.
         self.myMenu = self.menu.buildMenu()    -  Builds the main menu.
         self.menu.buildToolBar()               -  Builds the tool Bar.
         menu.buildContextMenu()                -  Builds the Context Menu.

         To add the mai9n menu - setMenuBar(self.myMenu)  I save a reference, so I can alter the visibility of the menu.
         To add the Tool bar   - self.addToolBar(self.menu.buildToolBar())  Creates a reference to the tool bar.

    """

    def __init__(self, myConfig, myLogger, eventsStore, parent=None):
        super().__init__(parent)

        self.config      = myConfig
        self.logger      = myLogger
        self.parent      = parent
        self.eventsStore = eventsStore

        self.toolbar      = QToolBar("Time Toolbar")
        self.context_menu = QMenu(self)
        self.selectTime   = st.SelectTime()
        self.styles       = styles.Styles()

        self.buildActions()

    # ----------------------------------------------------------------------------------------------------------------------- buildActions() --------
    def buildActions(self):
        """  Set up menu actions.
        """
        self.logger.info(" Building Menu Actions.")
        path = f"{RESOURCE_PATH}/digital-clock.png"
        self.actDigitalTime = QAction(QIcon(path),"Digital Time", self)
        self.actDigitalTime.triggered.connect(self.parent.setDigitalTime)

        path = f"{RESOURCE_PATH}/time-text.png"
        self.actTextTime = QAction(QIcon(path),"Time in words", self)
        self.actTextTime.triggered.connect(self.parent.setTextTime)
        self.actTextTime.setCheckable(False)

        path = f"{RESOURCE_PATH}/font.png"
        self.actFont = QAction(QIcon(path),"Change Font", self)
        self.actFont.triggered.connect(self.parent.openFontDialog)
        self.actFont.setCheckable(False)

        path = f"{RESOURCE_PATH}/colour-swatch.png"
        self.actBackColour = QAction(QIcon(path),"Change Background Colour", self)
        self.actBackColour.triggered.connect(self.parent.getBackColour)
        self.actBackColour.setCheckable(False)
        flag = False if self.config.TRANSPARENT else True
        self.actBackColour.setEnabled(flag)

        path = f"{RESOURCE_PATH}/colour.png"
        self.actForeColour = QAction(QIcon(path),"Change Foreground Colour", self)
        self.actForeColour.triggered.connect(self.parent.getForeColour)
        self.actForeColour.setCheckable(False)

        path = f"{RESOURCE_PATH}/cross.png"
        self.actClose = QAction(QIcon(path),"Close", self)
        self.actClose.triggered.connect(self.parent.close)                #  Close the app, which call the closeEvent (overridden).
        self.actClose.setCheckable(False)

        path = f"{RESOURCE_PATH}/gear.png"
        self.actSettings = QAction(QIcon(path),"Configure pyKlock", self)
        self.actSettings.triggered.connect(self.parent.openSettings)      #  Open the settings window.
        self.actSettings.setCheckable(False)

        self.actViewFriends = QAction("Friends", self)
        self.actViewFriends.triggered.connect(self.openFriendsViewer)

        self.actViewEvents = QAction("Events", self)
        self.actViewEvents.triggered.connect(self.openEventsViewer)

        self.actHelp = QAction("Help", self)
        self.actHelp.triggered.connect(self.parent.openHelpFile)

        self.actLicence = QAction("Licence", self)
        self.actLicence.triggered.connect(self.parent.openTextFile)

        self.actLogFile = QAction("Log File", self)
        self.actLogFile.triggered.connect(self.parent.openTextFile)

        self.actAbout = QAction("About", self)
        self.actAbout.triggered.connect(self.parent.openAbout)

        # Create the context menu and add some actions
        self.actToggleMenuBar = QAction("Toggle Menu Bar", self)
        self.actToggleMenuBar.triggered.connect(self.parent.toggleMenuBar)
        self.actToggleMenuBar.setCheckable(True)

        self.actToggleToolBar = QAction("Toggle Tool Bar", self)
        self.actToggleToolBar.triggered.connect(self.parent.toggleToolBar)
        self.actToggleToolBar.setCheckable(True)
    # ----------------------------------------------------------------------------------------------------------------------- buildMenu() -----------
    def buildMenu(self):
        # Set up main menu
        self.logger.info(" Building Menu")
        menu = QMenuBar()
        menu.setStyleSheet(self.styles.MENU_STYLE)

        mnuFile    = menu.addMenu("&File")
        mnuTime    = menu.addMenu("&Time")
        mnuDisplay = menu.addMenu("&Display")
        mnuThings = menu.addMenu("&Things")
        mnuHelp    = menu.addMenu("&Help")

        #  Set up menu actions.
        mnuFile.addAction(self.actSettings)
        mnuFile.addSeparator()
        mnuFile.addAction(self.actClose)

        mnuDisplay.addAction(self.actBackColour)
        mnuDisplay.addAction(self.actForeColour)
        mnuDisplay.addSeparator()
        mnuDisplay.addAction(self.actFont)
        mnuDisplay.addSeparator()
        mnuDisplay.addAction(self.actToggleMenuBar)
        mnuDisplay.addAction(self.actToggleToolBar)

        mnuTime.addAction(self.actDigitalTime)
        mnuTime.addAction(self.actTextTime)

        mnuThings.addAction(self.actViewFriends)
        mnuThings.addAction(self.actViewEvents)


        mnuHelp.addAction(self.actHelp)
        mnuHelp.addSeparator()
        mnuHelp.addAction(self.actLicence)
        mnuHelp.addAction(self.actLogFile)
        mnuHelp.addSeparator()
        mnuHelp.addAction(self.actAbout)

        return menu
    # ----------------------------------------------------------------------------------------------------------------------- buildToolBar() --------
    def buildToolBar(self):
        """  Set up toolbar.
             Uses the menu actions.
        """
        self.logger.info(" Building Tool Bar")
        self.toolbar.setIconSize(QSize(16, 16))
        self.toolbar.toggleViewAction().setEnabled(False)               #  to prevent this toolbar being removed.

        #  Set up tool bar actions.
        self.toolbar.addAction(self.actDigitalTime)
        self.toolbar.addAction(self.actTextTime)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.combo)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actFont)
        self.toolbar.addAction(self.actBackColour)
        self.toolbar.addAction(self.actForeColour)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actSettings)
        self.toolbar.addAction(self.actClose)

        return self.toolbar
    # ----------------------------------------------------------------------------------------------------------------------- buildContextMenu() ----
    def buildContextMenu(self):
        """  Set up the context
        """
        self.logger.info(" Building Context menu")
        self.context_menu.setStyleSheet("background   : transparent;")
        self.context_menu.addAction(self.actToggleMenuBar)
        self.context_menu.addAction(self.actToggleToolBar)
        self.context_menu.addSeparator()
        self.context_menu.addAction(self.actHelp)
        self.context_menu.addSeparator()
        self.context_menu.addAction(self.actClose)

        self.actToggleMenuBar.setChecked(self.parent.menu_bar)      #  Called in the parent.
        self.actToggleToolBar.setChecked(self.parent.tool_bar)      #  Maybe should be placed in here.
    # ----------------------------------------------------------------------------------------------------------------------- buildComboBox() -------
    def buildComboBox(self):
        """  Build the combo box - inserted into the main menu.
             Only used by the menu methods.
        """
        self.logger.info(" Building Combobox.")
        self.combo = QComboBox()
        self.combo.insertItems(1, self.selectTime.timeTypes)
        index = self.combo.findText(self.config.TIME_FORMAT)
        if index >= 0:
            self.combo.setCurrentIndex(index)

        self.combo.setStyleSheet("QComboBox"
                                 "{"
                                 "color        : self.foregroundColour;"
                                 "background   : transparent;"
                                 "border-radius: 3px;"
                                 "}")

    # ----------------------------------------------------------------------------------------------------------------------- openFriendsViewer() ---
    def openFriendsViewer(self):
        """   Open the friends viewer.
        """
        self.friendsViewer = fv.FriendsViewer(self.logger)
        self.friendsViewer.show()
    # ----------------------------------------------------------------------------------------------------------------------- openEventsViewer() ----
    def openEventsViewer(self):
        """   Open the event viewer.
        """
        self.eventsViewer = ev.EventsViewer(self.logger, self.config, self.eventsStore)
        self.eventsViewer.show()