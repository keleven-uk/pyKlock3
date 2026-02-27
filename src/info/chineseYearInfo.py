###############################################################################################################
#    chineseYearInfo   Copyright (C) <2026>  <Kevin Scott>                                                    #
#                                                                                                             #
#    The methods for displaying Chinese new Year info.                                                        #
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
# -*- coding: utf-8 -*-

import functools
import datetime

from pymeeus.Moon import Moon
from pymeeus.Sun import Sun

from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
                            QGroupBox, QGridLayout, QLabel, QSpinBox)
from PyQt6.QtCore    import Qt

# ----------------------------------------------------------------------------------------------------------------------- updateTime() --------------
def buildGUI(self):
    """  Build the GUI elements.
    """
    #  Create a central widget.

    self.centralWidget = QFrame()
    self.setCentralWidget(self.centralWidget)
    self.centralLayout = QVBoxLayout()
    self.ButtonLayout  = QHBoxLayout()

    self.cnyGroup    = QGroupBox("Chinese New Year")
    self.cnyLayout   = QGridLayout(self.cnyGroup)
    self.startText   = QLabel("New Year Date")
    self.startLabel  = QLabel("17 February 2026")
    self.hanText     = QLabel("Stem Branch - han")
    self.hanLabel    = QLabel("丙午")
    self.pinyinText  = QLabel("Stem Branch - pinyin")
    self.pinyinLabel = QLabel("bĭng-wŭ")
    self.animalText  = QLabel("Element Animal")
    self.animalLabel = QLabel("Fire Horse")
    self.aspectText  = QLabel("Aspect Yin/Yang")
    self.aspectLabel = QLabel("yang - year 43 of the cycle")
    self.dataText    = QLabel("Data")
    self.dataLabel   = QLabel("2026: 丙午 (bĭng-wŭ, Fire Horse; yang - year 43 of the cycle)")
    self.txtYear     = QLabel("Year")
    self.sbYear      = QSpinBox(self)

    self.cnyLayout.addWidget(self.startText,   0, 0, Qt.AlignmentFlag.AlignCenter)
    self.cnyLayout.addWidget(self.startLabel,  0, 1, Qt.AlignmentFlag.AlignLeft)
    self.cnyLayout.addWidget(self.hanText,     1, 0, Qt.AlignmentFlag.AlignCenter)
    self.cnyLayout.addWidget(self.hanLabel,    1, 1, Qt.AlignmentFlag.AlignLeft)
    self.cnyLayout.addWidget(self.pinyinText,  2, 0, Qt.AlignmentFlag.AlignCenter)
    self.cnyLayout.addWidget(self.pinyinLabel, 2, 1, Qt.AlignmentFlag.AlignLeft)
    self.cnyLayout.addWidget(self.animalText,  3, 0, Qt.AlignmentFlag.AlignCenter)
    self.cnyLayout.addWidget(self.animalLabel, 3, 1, Qt.AlignmentFlag.AlignLeft)
    self.cnyLayout.addWidget(self.aspectText,  4, 0, Qt.AlignmentFlag.AlignCenter)
    self.cnyLayout.addWidget(self.aspectLabel, 4, 1, Qt.AlignmentFlag.AlignLeft)
    self.cnyLayout.addWidget(self.aspectText,  4, 0, Qt.AlignmentFlag.AlignCenter)
    self.cnyLayout.addWidget(self.aspectLabel, 4, 1, Qt.AlignmentFlag.AlignLeft)
    self.cnyLayout.addWidget(self.dataText,    5, 0, Qt.AlignmentFlag.AlignCenter)
    self.cnyLayout.addWidget(self.dataLabel,   5, 1, Qt.AlignmentFlag.AlignLeft)
    self.cnyLayout.addWidget(self.txtYear,     6, 0, Qt.AlignmentFlag.AlignCenter)
    self.cnyLayout.addWidget(self.sbYear,      6, 1, Qt.AlignmentFlag.AlignLeft)

    currentYear = datetime.datetime.now().year

    self.sbYear.setMinimum(1)
    self.sbYear.setMaximum(3000)
    self.sbYear.setValue(currentYear)

    #  callback needed to pass self as argument to update()
    sbYearCallback = functools.partial(update, self)
    self.sbYear.valueChanged.connect(sbYearCallback)

    self.cnyGroup.setLayout(self.cnyLayout)

    btnClose = QPushButton(text="Close", parent=self)
    btnClose.clicked.connect(self.close)

    self.ButtonLayout.addWidget(btnClose)

    self.centralLayout.addWidget(self.cnyGroup)
    self.centralLayout.addLayout(self.ButtonLayout)

    self.centralWidget.setLayout(self.centralLayout)
# ----------------------------------------------------------------------------------------------------------------------- closeEvent() ----------
def update(self):
    """  Updated the labels.
    """
    self.data         = calculate(self.sbYear.value()) 
    self.year         = self.data[0]
    self.stemHan      = self.data[1]
    self.branchHan    = self.data[2]
    self.stemPinyin   = self.data[3]
    self.branchPinyin = self.data[4]
    self.element      = self.data[5]
    self.animal       = self.data[6]
    self.aspect       = self.data[7]
    self.index        = self.data[8]

    self.startLabel.setText(findNewYearDate(self.year))
    self.hanLabel.setText(f"{self.stemHan} {self.branchHan}")
    self.pinyinLabel.setText(f"{self.stemPinyin} {self.branchPinyin}")
    self.animalLabel.setText(f"{self.element}-{self.animal}")
    self.aspectLabel.setText(f"{self.aspect} - Year {self.index} of the cycle")
    self.dataLabel.setText(f"{self.year} : {self.stemHan}{self.branchHan}  ({self.stemPinyin}-{self.branchPinyin},  {self.element} {self.animal};  {self.aspect} - year {self.index} of the cycle)")
#  ----------------------------------------------------------------------------------------------------------------------- data for calculate -------
#  The data and the calculate method was gratefully copied from #  https://rosettacode.org/wiki/Chinese_zodiac#Python

pinyin = {
  "甲": "jiă",
  "乙": "yĭ",
  "丙": "bĭng",
  "丁": "dīng",
  "戊": "wù",
  "己": "jĭ",
  "庚": "gēng",
  "辛": "xīn",
  "壬": "rén",
  "癸": "gŭi",

  "子": "zĭ",
  "丑": "chŏu",
  "寅": "yín",
  "卯": "măo",
  "辰": "chén",
  "巳": "sì",
  "午": "wŭ",
  "未": "wèi",
  "申": "shēn",
  "酉": "yŏu",
  "戌": "xū",
  "亥": "hài"
}

animals = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
           "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
elements = ["Wood", "Fire", "Earth", "Metal", "Water"]

celestial = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
terrestrial = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
aspects = ["yang", "yin"]

# ----------------------------------------------------------------------------------------------------------------------- calculate() ---------------
def calculate(year):
    """  Calculates the chinese New Year info.
    """
    BASE = 4
    year = int(year)
    cycle_year = year - BASE
    stem_number = cycle_year % 10
    stem_han = celestial[stem_number]
    stem_pinyin = pinyin[stem_han]
    element_number = stem_number // 2
    element = elements[element_number]
    branch_number = cycle_year % 12
    branch_han = terrestrial[branch_number]
    branch_pinyin = pinyin[branch_han]
    animal = animals[branch_number]
    aspect_number = cycle_year % 2
    aspect = aspects[aspect_number]
    index = cycle_year % 60 + 1
    return [year, stem_han, branch_han, stem_pinyin, branch_pinyin, element, animal, aspect, index]
# ----------------------------------------------------------------------------------------------------------------------- findNewYearDate() ---------
def findNewYearDate(year: int):
    """  Determines the start of the Chinese New Year.

        Copied from https://www.krootl.com/blog/working-with-lunar-calendar-in-python
    """
    askedYear = year
    year -= 1
    equinox = Sun.get_equinox_solstice(year, target="winter")
    lowerLimit = datetime.datetime(askedYear, 1, 21)
    phase = Moon.moon_phase(equinox, target="new")
    newMoonDate = datetime.datetime(*phase.get_full_date()[:5])
    while newMoonDate < lowerLimit or newMoonDate.date() == lowerLimit.date():
        equinox = phase + 29
        phase = Moon.moon_phase(equinox, target="new")
        newMoonDate = datetime.datetime(*phase.get_full_date()[:5])

    return newMoonDate.strftime("%d %B %Y")

