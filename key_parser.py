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

from termcolor import colored
import sys
sys.path.append(directory + "/ResearchAnalyzer")
from common import *

sys.path.append(directory + "/ResearchLogger/PyKeylogger-1.2.1")
from constants import *


class KeyParser:
    """
        Class for parsing the key data from a session.
    """

    def __init__(self, keys_filename, search_pattern=''):
        """
        - keys_filename is the path of the logfile.
        - search_pattern is used to indicate which window to pay attention to.
        the empty string indicates: pay attention to all clicks in all windows.
        """
        self.keys_filename = keys_filename
        self.keys = []
        self._set_keys(search_pattern)

    def _set_keys(self, title=''):
        """
            Reads the detailed logfile and saves the data to the list self.keys
        """
        f = open(self.keys_filename, 'r')
        line = f.readline()
        while line != '' and line != '\n':
            # Get attributes from the log line.
            date, time, program_name, window_id, username, window_title, logged_keys = line.split(
                ATTRIBUTE_SEPARATOR)
            # Check whether the title is in the window.
            if title in window_title:
                logged_keys = logged_keys.split(LINE_SEPARATOR)
                # Withdraw last element since it is '\n'
                try:
                    logged_keys.remove('\n')
                except ValueError:
                    pass
                # Save the raw data.
                for logged_key in logged_keys:
                    ms, key, msg, x, y = logged_key.split(DATA_SEPARATOR)
                    self.keys += [(date, time, program_name, username, window_id,
                                   window_title, ms, key, msg, x, y)]
            line = f.readline()
            for k in self. keys:
                if 'down' in k[9]:
                    print k[8]

    def pretty_printer(self):
        """
        Prints the keys raw log in a readable way.
        """
        for k in self.keys:
            date, time, program_name, username, window_id, window_title, time, key, msg, coordx, coordy = k
            print date, time, program_name, colored(window_id, 'red'), username, window_title, colored(time, 'yellow'), colored(key, 'blue'), msg, coordx, coordy
