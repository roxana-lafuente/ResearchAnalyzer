# !/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
#
# ResearchAnalyzer: Data Analyzer for ResearchLogger
# Copyright (C) 2015  Roxana Lafuente <roxana.lafuente@gmail.com>
#
# ResearchAnalyzer is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# ResearchAnalyzer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################

TS = "Sesión de traducción"

# , "SMD-20", "SMI-20", "CMD-20", "Baseline", "SMD-10"]
EXPERIMENTS = ["CMD-20"]

# subjects = ["P10112014-1", "P24102014-2", "P23102014-2", "P30102014-1"]
# subjects += ["P18122014-1", "P30102014-2", "P23102014-1", "P17112014-1"]
# subjects += ["P31102014-3", "P31102014-1", "P23102014-4", "P31102014-2"]
# subjects += ["P23102014-3", "P27112014-1", "P24102014-1"]

# Nautilus order
# SUBJECTS = ["P10112014-1", "P24102014-2", "P23102014-2", "P30102014-1"]
# SUBJECTS += ["P18122014-1", "P30102014-2", "P23102014-1", "P17112014-1"]
# SUBJECTS += ["P31102014-1", "P23102014-4", "P31102014-2"]
# SUBJECTS += ["P23102014-3", "P27112014-1", "P24102014-1"] # "P31102014-3"
# Excel order
SUBJECTS = ["P23102014-4", "P23102014-2", "P23102014-3", "P31102014-2"]
SUBJECTS += ["P18122014-1", "P24102014-2", "P24102014-1", "P30102014-1"]
SUBJECTS += ["P31102014-1", "P17112014-1", "P27112014-1"]
SUBJECTS += ["P10112014-1", "P23102014-1", "P30102014-2"]  # "P31102014-3"

LINE_LENGHT = 80

REPLACE_KEYS = {'space',
                'apostrophe',
                'plus',
                'comma',
                'minus',
                'period',
                '0',
                '1',
                '2',
                '3',
                '4',
                '5',
                '6',
                '7',
                '8',
                '9',
                'less',
                'a',
                'b',
                'c',
                'd',
                'e',
                'f',
                'g',
                'h',
                'i',
                'j',
                'k',
                'l',
                'm',
                'n',
                'o',
                'p',
                'q',
                'r',
                's',
                't',
                'u',
                'v',
                'w',
                'x',
                'y',
                'z',
                'exclamdown',
                'ccedilla',
                'ntilde',
                'masculine',
                'return',
                'asterisk',
                'slash',
                }

FUNCTION_KEYS = {
    'grave',
    'acute',
    'altr',
    'tab',
    'pause',
    'bloq_despl',
    'escape',
    'repag',
    'screenshot',
    'insert',
    'bloq_num',
    'f1',
    'f2',
    'f3',
    'f4',
    'f5',
    'f6',
    'f7',
    'f8',
    'f9',
    'f10',
    'f11',
    'f12',
    'shiftl',
    'shiftr',
    'ctrll',
    'ctrlr',
    'mayus',
    'altl',
}

MOVE_KEYS = {
    'begin',
    'leftarrow',
    'uparrow',
    'rightarrow',
    'downarrow',
    'avpag',
    'end',
}

ERASE_KEYS = {
    'backspace',
    'supr',
}

# 'click',
# 'cancel',
# 'windows',
# 'browser',
# 'favorite',
# 'f5',
# 'mail',
# 'calc',
# 'suspend',
# 'mplayer',
# 'mute',
# 'next',
# 'previous',
# 'vdown',
# 'vup',
# 'play_pause'
