# !/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
#
# ResearchAnalyzer: Data Analyzer for ResearchLogger
# Copyright (C) 2015  Roxana Lafuente <roxana.lafuente@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# Get the absolute path to the test files in the directory variable
from inspect import getsourcefile
from os.path import abspath, dirname
directory = dirname(dirname(abspath(getsourcefile(lambda: 0))))

from common import *
from termcolor import colored

import sys
sys.path.append(directory + "/ResearchLogger/PyKeylogger-1.2.1")
from constants import *


class ClickParser:
    """
        Class for parsing the click data from a session.
    """

    def __init__(self, clicks_filename, search_pattern=''):
        """
        - clicks_filename is the path of the logfile.
        - search_pattern is used to indicate which window to pay attention to.
        the empty string indicates: pay attention to all clicks in all windows.
        """
        self.clicks_filename = clicks_filename
        self.clicks = []
        self._set_clicks(search_pattern)

    def _set_clicks(self, title=''):
        """
            Saves in self.clicks a list with all the lines in the log that
        belong to a certain window. This is selected by the title parameter.
        If title is not provided, then title is set to '' so that all the lines
        in the log are selected.
        """
        f = open(self.clicks_filename, 'r')
        line = f.readline()
        while line != '' and line != '\n':
            date, real_time, program_name, window_id, username, window_title, resolution, logged_clicks = line.split(
                ATTRIBUTE_SEPARATOR)
            if title in window_title:
                logged_clicks = logged_clicks.split(LINE_SEPARATOR)
                # Withdraw last element since it is '\n'
                logged_clicks = logged_clicks[:-1]
                for logged_click in logged_clicks:
                    xcoord, ycoord, miliseconds, msg, img_name = logged_click.split(
                        DATA_SEPARATOR)
                    self.clicks += [(date, real_time, program_name, username,
                                     window_id, window_title, miliseconds, msg,
                                     xcoord, ycoord, resolution, img_name)]
            line = f.readline()

    def pretty_printer(self):
        """
            Prints the clicks raw log in a readable way.
        """
        self.screen = []
        # Set clicks
        for click_struct in self.clicks:
            date, real_time, program_name, username, window_id, window_title, miliseconds, msg, xcoord, ycoord, resolution, image = click_struct
            print date, real_time, program_name, colored(username, 'red'), window_id, colored(window_title, 'blue'), colored(miliseconds, 'yellow'), msg, xcoord, ycoord, resolution, image
