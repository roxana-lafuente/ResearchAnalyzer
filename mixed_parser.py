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
directory = dirname(dirname(dirname(abspath(getsourcefile(lambda: 0)))))

import sys
sys.path.append(directory + "/ResearchAnalyzer")
from key_parser import KeyParser
from click_parser import ClickParser
import copy


class Parser(KeyParser, ClickParser):
    """
        Class for parsing the User Activity Data from a session.
    """

    def __init__(self, keys_filename, clicks_filename, search_pattern=''):
        """
        - keys_filename is the path of the log (keys)
        - clicks_filename is the path of the log (clicks)
        - search_pattern is used to filter the window names
        """
        self.keys_filename = keys_filename
        self.clicks_filename = clicks_filename
        self.keys = []
        self.clicks = []
        self.merged = []
        self._set_keys(search_pattern)
        self._set_clicks(search_pattern)
        self._merge_clicks_and_keys_logs()

    def _merge_clicks_and_keys_logs(self):
        """
        Merges click and mouse logs ordered by the millisecond they occurred
        in.
        """
        # Get keys and clicks statistics.
        processed_keys = self.keys
        processed_clicks = self.clicks
        # Create key_dict has both keys and clicks.
        # We do this because we need the list to be ordered by time.
        self.key_dict = dict({})
        for pkey in processed_keys:
            date, time, program_name, username, window_id, window_title, ms, key, msg, x, y = pkey
            self.key_dict[ms] = pkey
        for pclick in processed_clicks:
            date, real_time, program_name, username, window_id, window_title, ms, msg, x, y, resolution, img_name = pclick
            self.key_dict[ms] = pclick
        # Now we add the content to the real structure.
        for k in sorted(self.key_dict.keys()):
            self.merged += [self.key_dict[k]]

    def pretty_printer(self):
        """
        Prints the merged clicks and keys raw log in a readable way.
        """
        for time in sorted(self.uad):
            type, date, clock_time, program, user, window_id, title, millisecond, key, msg, x, y = self.uad[
                time]
            print colored(key, 'red') + SEP + millisecond + SEP + msg + SEP + title + SEP + program
        SEP = ' - '
        return table
