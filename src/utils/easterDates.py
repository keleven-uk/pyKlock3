###############################################################################################################
#    easterDates.py   Copyright (C) <2026>  <Kevin Scott>                                                     #
#                                                                                                             #
#    Functions to determine Easter Sunday                                                                     #
#                                                                                                             #
#    For changes see history.txt                                                                              #
#                                                                                                             #
#    Source - https://stackoverflow.com/a/78259311                                                            #
#    Posted by dan04                                                                                          #
#    Retrieved 2026-02-19, License - CC BY-SA 4.0                                                             #
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
# -*- coding: utf-8 -*-v

import datetime

def hebrew_easter(year):
    """  This is the Sunday that falls during Passover.
    """
    lunation = (235 * year + 6) // 19 - 9
    week, molad = divmod(765433 * lunation + 65451, 181440)
    if (7 * year + 6) % 19 < 12 and (molad >= 172000):
        week += 1
    return datetime.date.fromordinal(week * 7)

def julian_easter(year):
    """  The Council of Nicea in 325 CE decided not to use the actual Jewish calendar to set the date of Easter, 
         but to perform their own calculation.
         Valid in dates after 326 AD
    """
    leap_months = (7 * year + 8) // 19 - 9
    week = ((6725 * year + 18) // 19 + 30 * leap_months + year // 4 + 5) // 7
    return datetime.date.fromordinal(week * 7)

def gregorian_easter(year):
    """  Valid in years 1583 to 4099.
    """
    century = year // 100
    lunar_adj = (8 * century + 13) // 25
    solar_adj = -century + century // 4
    total_adj = solar_adj + lunar_adj
    leap_months = (210 * year - year % 19 + 19 * total_adj + 266) // 570
    full_moon = (6725 * year + 18) // 19 + 30 * leap_months - lunar_adj + year // 4 + 3
    if 286 <= (total_adj + year % 19 * 11) % 30 * 19 - year % 19 <= 312:
        full_moon -= 1
    week = full_moon // 7 - 38
    return datetime.date.fromordinal(week * 7)

