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

# Subjects
subjects = ["P23102014-1", "P23102014-2", "P23102014-3", "P23102014-4"]
subjects += ["P24102014-1", "P24102014-2", "P30102014-1", "P30102014-2"]
subjects += ["P31102014-1", "P31102014-2", "P31102014-3", "P10112014-1"]
subjects += ["P17112014-1", "P27112014-1", "P18122014-1"]
# Base Dir
baseDir = '../../Logs/Baseline/'
# Experiment
experiment = '-baseline-'


def getUADKeys(keys, searchpattern=''):
    """
        Get a sorted list of the keys in the dictionary self.uad.
    """
    all_keys = keys.keys()
    all_keys = sorted(all_keys, key=lambda x: int(x))
    # Only the keys whose data match the pattern.
    keys = [key for key in all_keys if searchpattern in keys[key]]
#    print keys
#    print '794583' in keys
    return keys


def getWords(text):
    SPACES = [' ', '\n', '\t']
    ltext = []
    tmp = ''
    for letter in text:
        if letter not in SPACES:
            tmp += letter
        else:
            if tmp not in SPACES:
                ltext += [tmp]
            tmp = ''
    return ltext


def convert_to_hex(s):
    r = str(s)
    if len(r) == 4:
        r = r[:2] + r[1] + r[2:3] + r[2] + r[3:] + r[3]
    return r


def clear():
    for i in range(10):
        print
