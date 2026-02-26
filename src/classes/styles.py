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
            background-color: black;
            width : 134px
            }
        """

    @property
    def QGroupBox_STYLE(self):
        return"""
        QGroupBox {
            background: black;
            border: 2px solid gray;
            border-radius: 5px;
            }
        """

    @property
    def QGroupBox_STYLE(self):
        return """
        
        """
    QSpinBox,
    QDateTimeEdit 
    {
        background-color: #131313;
        color : #eee;
        border: 1px solid #343434;
        padding: 3px;
        padding-left: 5px;
        border-radius : 2px;

    }


    QSpinBox::up-button, 
    QDateTimeEdit::up-button
    {
        border-top-right-radius:2px;
        background-color: #777777;
        width: 16px; 
        border-width: 1px;

    }


    QSpinBox::up-button:hover, 
    QDateTimeEdit::up-button:hover
    {
        background-color: #585858;

    }


    QSpinBox::up-button:pressed, 
    QDateTimeEdit::up-button:pressed
    {
        background-color: #252525;
        width: 16px; 
        border-width: 1px;

    }


    QSpinBox::up-arrow,
    QDateTimeEdit::up-arrow
    {
        image: url(://arrow-up.png);
        width: 7px;
        height: 7px;

    }


    QSpinBox::down-button, 
    QDateTimeEdit::down-button
    {
        border-bottom-right-radius:2px;
        background-color: #777777;
        width: 16px; 
        border-width: 1px;

    }


    QSpinBox::down-button:hover, 
    QDateTimeEdit::down-button:hover
    {
        background-color: #585858;

    }


    QSpinBox::down-button:pressed, 
    QDateTimeEdit::down-button:pressed
    {
        background-color: #252525;
        width: 16px; 
        border-width: 1px;

    }


    QSpinBox::down-arrow,
    QDateTimeEdit::down-arrow
    {
        image: url(://arrow-down.png);
        width: 7px;
        height: 7px;

    }


