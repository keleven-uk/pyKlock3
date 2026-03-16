###############################################################################################################
#    textKlock.py    Copyright (C) <2026>  <Kevin Scott>                                                      #
#                                                                                                             #
#    A class that displays the time within a matrix of words.                                                 #
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
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QApplication, QFrame, QMainWindow, 
                             QGroupBox, QLabel)


class textKlock(QMainWindow):
    """  A class that displays the time within a matrix of words.
    """
    def __init__(self, myConfig):
        super().__init__()

        self.config     = myConfig
        self.onColour   = self.config.TK_ON_COLOUR
        self.offColour  = self.config.TK_OFFOLOUR
        self.backColour = self.config.TK_BACKGROUND

        height     = 600
        width      = 400
        screenSize = QApplication.primaryScreen().availableGeometry()
        xPos       = int((screenSize.width() / 2)  - (width / 2))
        yPos       = int((screenSize.height() / 2) - (height / 2))

        self.setGeometry(xPos, yPos, height, width)
        self.setWindowTitle("pyKlock")

        self.buildGUI()

        self.it("ON")
        self.iss("ON")
        self.half("ON")
        self.quarter("ON")
        self.one("ON")
        self.two("ON")
        self.three("ON")
        self.four("ON")
        self.five("ON")
        self.six("ON")
        self.seven("ON")
        self.eight("ON")
        self.nine("ON")
        self.ten("ON")
        self.eleven("ON")
        self.twelve("ON")

    def buildGUI(self):
        """  Build the GUI elements.
        """
        centralWidget = QFrame()
        self.setCentralWidget(centralWidget)
        centralLayout = QVBoxLayout()
        ButtonLayout  = QHBoxLayout()

        tkGroup  = QGroupBox("Text Klock")
        tkLayout = QGridLayout(tkGroup)
        
        self.addRow(tkLayout, ["I", "T", "E", "E", "I", "S", "K", "A", "T", "E", "N", "H", "A", "L", "F", "Q", "U", "A", "R", "T", "E", "R", "I", "X"], 0)
        self.addRow(tkLayout, ["T", "W", "E", "N", "T", "Y", "K", "F", "I", "V", "E", "J", "A", "B", "O", "U", "T", "P", "T", "O", "S", "F", "E", "W"], 1)
        self.addRow(tkLayout, ["P", "A", "S", "T", "K", "O", "N", "E", "L", "T", "W", "O", "O", "T", "H", "R", "E", "E", "C", "F", "O", "U", "R", "K"], 2)
        self.addRow(tkLayout, ["F", "I", "V", "E", "D", "S", "I", "X", "U", "S", "E", "V", "E", "N", "R", "E", "I", "G", "H", "T", "M", "T", "E", "N"], 3)
        self.addRow(tkLayout, ["N", "I", "N", "E", "K", "E", "L", "E", "V", "E", "N", "U", "T", "W", "E", "L", "V", "E", "T", "A", "S", "H", "O", "W"], 4)
        self.addRow(tkLayout, ["I", "N", "X", "I", "N", "T", "H", "E", "L", "O", "N", "I", "A", "F", "T", "E", "R", "N", "O", "O", "N", "T", "J", "C"], 5)
        self.addRow(tkLayout, ["G", "S", "I", "P", "B", "O", "M", "O", "R", "N", "I", "N", "G", "Q", "Z", "F", "U", "P", "G", "B", "F", "O", "T", "H"], 6)
        self.addRow(tkLayout, ["E", "V", "E", "N", "I", "N", "G", "N", "M", "O", "V", "E", "A", "X", "Z", "X", "M", "I", "D", "N", "I", "G", "H", "T"], 7)

        btnClose = QPushButton(text="Close", parent=self)
        btnClose.clicked.connect(self.close)

        ButtonLayout.addWidget(btnClose)

        centralLayout.addWidget(tkGroup)
        centralLayout.addLayout(ButtonLayout)

        centralWidget.setLayout(centralLayout)

    # ----------------------------------------------------------------------------------------------------------------------- addRow() --------------
    def addRow(self, layout, row, rowCount):
        column = 0
        for element in row:
            label = QLabel(element)
            name = f"{column}:{rowCount}"
            label.setObjectName(name)
            #label.setFixedWidth(self.size)
            label.adjustSize()
            label.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            layout.addWidget(label, rowCount, column)
            column += 1
    # ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
    def closeEvent(self, event):
        event.accept()
    # ----------------------------------------------------------------------------------------------------------------------- one() -----------------
    def one(self, mode):
        o = self.findChild(QLabel, "5:2")
        n = self.findChild(QLabel, "6:2")
        e = self.findChild(QLabel, "7:2")

        if mode == "ON":
            o.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        else:
            o.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
    # ----------------------------------------------------------------------------------------------------------------------- two() -----------------
    def two(self, mode):
        t = self.findChild(QLabel, "9:2")
        w = self.findChild(QLabel, "10:2")
        o = self.findChild(QLabel, "11:2")

        if mode == "ON":
            t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            w.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            o.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        else:
            t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            w.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            o.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
    # ----------------------------------------------------------------------------------------------------------------------- three() ---------------
    def three(self, mode):
        t = self.findChild(QLabel, "13:2")
        h = self.findChild(QLabel, "14:2")
        r = self.findChild(QLabel, "15:2")
        e = self.findChild(QLabel, "16:2")
        f = self.findChild(QLabel, "17:2")      #  Second e

        if mode == "ON":
            t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            h.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            r.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        else:
            t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            h.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            r.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
    # ----------------------------------------------------------------------------------------------------------------------- four() ----------------
    def four(self, mode):
        f = self.findChild(QLabel, "19:2")
        o = self.findChild(QLabel, "20:2")
        u = self.findChild(QLabel, "21:2")
        r = self.findChild(QLabel, "22:2")

        if mode == "ON":
            f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            o.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            u.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            r.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        else:
            f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            o.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            u.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            r.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
    # ----------------------------------------------------------------------------------------------------------------------- five() ----------------
    def five(self, mode):
        f = self.findChild(QLabel, "0:3")
        i = self.findChild(QLabel, "1:3")
        v = self.findChild(QLabel, "2:3")
        e = self.findChild(QLabel, "3:3")

        if mode == "ON":
            f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            v.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        else:
            f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            v.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
    # ----------------------------------------------------------------------------------------------------------------------- six() -----------------
    def six(self, mode):
        s = self.findChild(QLabel, "5:3")
        i = self.findChild(QLabel, "6:3")
        x = self.findChild(QLabel, "7:3")

        if mode == "ON":
            s.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            x.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        else:
            s.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            x.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
    # ----------------------------------------------------------------------------------------------------------------------- seven() ---------------
    def seven(self, mode):
        s = self.findChild(QLabel, "9:3")
        e = self.findChild(QLabel, "10:3")
        v = self.findChild(QLabel, "11:3")
        f = self.findChild(QLabel, "12:3")      #  Second e
        n = self.findChild(QLabel, "13:3")

        if mode == "ON":
            s.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            v.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        else:
            s.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            v.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
    # ----------------------------------------------------------------------------------------------------------------------- eight() ---------------
    def eight(self, mode):
        e = self.findChild(QLabel, "15:3")
        i = self.findChild(QLabel, "16:3")
        g = self.findChild(QLabel, "17:3")
        h = self.findChild(QLabel, "18:3")
        t = self.findChild(QLabel, "19:3")

        if mode == "ON":
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            g.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            h.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        else:
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            g.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            h.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
    # ----------------------------------------------------------------------------------------------------------------------- nine() ----------------
    def nine(self, mode):
        n = self.findChild(QLabel, "0:4")
        i = self.findChild(QLabel, "1:4")
        o = self.findChild(QLabel, "2:4")      #  Second n
        e = self.findChild(QLabel, "3:4")

        if mode == "ON":
            n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            o.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        else:
            n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            o.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
    # ----------------------------------------------------------------------------------------------------------------------- ten() -----------------
    def ten(self, mode):
        t = self.findChild(QLabel, "21:3")
        e = self.findChild(QLabel, "22:3")
        n = self.findChild(QLabel, "23:3")

        if mode == "ON":
            t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        else:
            t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
    # ----------------------------------------------------------------------------------------------------------------------- eleven() --------------
    def eleven(self, mode):
        e = self.findChild(QLabel, "5:4")
        l = self.findChild(QLabel, "6:4")
        f = self.findChild(QLabel, "7:4")      #  Second e
        v = self.findChild(QLabel, "8:4")
        g = self.findChild(QLabel, "9:4")      #  Third e
        n = self.findChild(QLabel, "10:4")

        if mode == "ON":
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            l.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            v.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            g.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        else:
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            l.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            v.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            g.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
    # ----------------------------------------------------------------------------------------------------------------------- twelve() --------------
    def twelve(self, mode):
        t = self.findChild(QLabel, "12:4")
        w = self.findChild(QLabel, "13:4")
        e = self.findChild(QLabel, "14:4")
        l = self.findChild(QLabel, "15:4")
        v = self.findChild(QLabel, "16:4")
        f = self.findChild(QLabel, "17:4")      #  Second e

        if mode == "ON":
            t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            w.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            l.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            v.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        else:
            t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            w.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            l.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            v.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
    # ----------------------------------------------------------------------------------------------------------------------- it() ------------------
    def it(self, mode):
        i = self.findChild(QLabel, "0:0")
        t = self.findChild(QLabel, "1:0")

        if mode == "ON":
            i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        else:
            i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
    # ----------------------------------------------------------------------------------------------------------------------- is() ------------------
    def iss(self, mode):
        """  is = reserved word in python.
        """
        i = self.findChild(QLabel, "4:0")
        s = self.findChild(QLabel, "5:0")

        if mode == "ON":
            i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            s.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        else:
            i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            s.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
    # ----------------------------------------------------------------------------------------------------------------------- half() ----------------
    def half(self, mode):
        h = self.findChild(QLabel, "11:0")
        a = self.findChild(QLabel, "12:0")
        l = self.findChild(QLabel, "13:0")
        f = self.findChild(QLabel, "14:0")

        if mode == "ON":
            h.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            a.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            l.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        else:
            h.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            a.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            l.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
    # ----------------------------------------------------------------------------------------------------------------------- quarter() ----------------
    def quarter(self, mode):
        q = self.findChild(QLabel, "15:0")
        u = self.findChild(QLabel, "16:0")
        a = self.findChild(QLabel, "17:0")
        r = self.findChild(QLabel, "18:0")
        t = self.findChild(QLabel, "19:0")
        e = self.findChild(QLabel, "20:0")
        s = self.findChild(QLabel, "21:0")      #  Second e

        if mode == "ON":
            q.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            u.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            a.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            r.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
            s.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        else:
            q.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            u.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            a.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            r.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
            s.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")