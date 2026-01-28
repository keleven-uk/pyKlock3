###############################################################################################################
#    progressBarStyles   Copyright (C) <2025-26>  <Kevin Scott>                                               #
#                                                                                                             #
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

class Styles():
    """  A set of styles for the battery progress bar.
         This enables for the progress bar to change colour depending upon state and charge.
    """
    @property
    def RUNNING_ON_AC_STYLE(self):
        return """
        QProgressBar{
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
            font: bold 10px;
        }

        QProgressBar::chunk {
            background-color: lightblue;
            width: 10px;
            margin: 1px;
        }
        """

    @property
    def BATTERY_LOW_STYLE(self):
     return """
        QProgressBar{
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
            font: bold 10px;
        }

        QProgressBar::chunk {
            background-color: red;
            width: 10px;
            margin: 1px;
        }
        """
    @property
    def RUNNING_ON_BATTERY_STYLE(self):
     return """
        QProgressBar{
            color: black;
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
            font: bold 10px;
        }

        QProgressBar::chunk {
            background-color: green;
            width: 10px;
            margin: 1px;
        }
        """

    @property
    def CHARGING_STYLE(self):
        return """
        QProgressBar{
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
            font: bold 10px;
        }

        QProgressBar::chunk {
            background-color: blue;
            width: 10px;
            margin: 1px;
        }
        """

    @property
    def BATTERY_FULL_STYLE(self):
        return """
        QProgressBar{
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
            font: bold 10px;
        }

        QProgressBar::chunk {
            background-color: yellow;
            width: 10px;
            margin: 1px;
        }
        """

    @property
    def MENU_STYLE(self):
        return """
        QMenu {
            color     : green;
            background: transparent;
        }

        QMenu::item{
            color     : blue;
            background: transparent;
        }
        """

    @property
    def QToggle_STYLE(self):
        return """
        QToggle{
            qproperty-bg_color      :#111;
            qproperty-circle_color  :#DDF;
            qproperty-active_color  :#AAF;
            qproperty-disabled_color:#777;
            qproperty-text_color    :#A0F;
            }
        """

    @property
    def QEdit_STYLE(self):
        return"""
        QLineEdit{
            border : 1px solid ;
            border-color : grey
            }
        """

    @property
    def QDateEdit_STYLE(self):
        return"""
        QDateEdit{
            width : 134px
            }
        """

    @property
    def QTimeEdit_STYLE(self):
        return"""
        QTimeEdit{
            width : 134px
            }
        """

    @property
    def QComboBox_STYLE(self):
        return"""
        QComboBox{
            width : 134px
            }
        """