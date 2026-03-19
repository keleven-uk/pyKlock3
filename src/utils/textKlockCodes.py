###############################################################################################################
#    textKlockCodes.py    Copyright (C) <2026>  <Kevin Scott>                                                 #
#                                                                                                             #
#    AThe methods to switch ON/OFF the text for textKlock.                                                    #
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

from PyQt6.QtWidgets import QLabel

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
# ----------------------------------------------------------------------------------------------------------------------- inn() -----------------
def inn(self, mode):
    """  in = reserved word in python.
    """
    i = self.findChild(QLabel, "0:5")
    n = self.findChild(QLabel, "1:5")

    if mode == "ON":
        i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
    else:
        i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
# ----------------------------------------------------------------------------------------------------------------------- the() -----------------
def the(self, mode):
    t = self.findChild(QLabel, "5:5")
    h = self.findChild(QLabel, "6:5")
    e = self.findChild(QLabel, "7:5")

    if mode == "ON":
        t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        h.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
    else:
        t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        h.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
# ----------------------------------------------------------------------------------------------------------------------- on() ------------------
def on(self, mode):
    o = self.findChild(QLabel, "9:5")
    n = self.findChild(QLabel, "10:5")

    if mode == "ON":
        o.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
    else:
        o.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
# ----------------------------------------------------------------------------------------------------------------------- after() ---------------
def after(self, mode):
    a = self.findChild(QLabel, "12:5")
    f = self.findChild(QLabel, "13:5")
    t = self.findChild(QLabel, "14:5")
    e = self.findChild(QLabel, "15:5")
    r = self.findChild(QLabel, "16:5")

    if mode == "ON":
        a.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        r.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
    else:
        a.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        r.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
# ----------------------------------------------------------------------------------------------------------------------- noon() ----------------
def noon(self, mode):
    n = self.findChild(QLabel, "17:5")
    o = self.findChild(QLabel, "18:5")
    p = self.findChild(QLabel, "19:5")      #  Second o
    q = self.findChild(QLabel, "20:5")      #  Second n

    if mode == "ON":
        n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        o.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        p.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        q.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
    else:
        n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        o.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        p.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        q.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
# ----------------------------------------------------------------------------------------------------------------------- noon() ----------------
def morning(self, mode):
    m = self.findChild(QLabel, "6:6")
    o = self.findChild(QLabel, "7:6")
    r = self.findChild(QLabel, "8:6")
    n = self.findChild(QLabel, "9:6")
    i = self.findChild(QLabel, "10:6")
    p = self.findChild(QLabel, "11:6")      #  Second n
    g = self.findChild(QLabel, "12:6")

    if mode == "ON":
        m.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        o.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        r.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        p.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        g.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
    else:
        m.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        o.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        r.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        p.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        g.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
# ----------------------------------------------------------------------------------------------------------------------- evening() -------------
def evening(self, mode):
    e = self.findChild(QLabel, "0:7")
    v = self.findChild(QLabel, "1:7")
    f = self.findChild(QLabel, "2:7")      #  Second e
    n = self.findChild(QLabel, "3:7")
    i = self.findChild(QLabel, "4:7")
    p = self.findChild(QLabel, "5:7")      #  Second n
    g = self.findChild(QLabel, "6:7")

    if mode == "ON":
        e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        v.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        p.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        g.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
    else:
        e.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        v.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        f.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        p.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        g.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
# ----------------------------------------------------------------------------------------------------------------------- midnight() ------------
def midnight(self, mode):
    m = self.findChild(QLabel, "16:7")
    i = self.findChild(QLabel, "17:7")
    d = self.findChild(QLabel, "18:7")
    n = self.findChild(QLabel, "19:7")
    j = self.findChild(QLabel, "20:7")      #  Second n
    g = self.findChild(QLabel, "21:7")
    h = self.findChild(QLabel, "22:7")
    t = self.findChild(QLabel, "23:7")

    if mode == "ON":
        m.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        d.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        j.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        g.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        h.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
        t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.onColour}; background-color: {self.backColour}")
    else:
        m.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        i.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        d.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        n.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        j.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        g.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        h.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")
        t.setStyleSheet(f"padding: 0px; margin: 0px; color: {self.offColour}; background-color: {self.backColour}")