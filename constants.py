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

BASE_PATH = '.'

SYSLOG = 'system_log'

LINE_SEPARATOR = " "
ATTRIBUTE_SEPARATOR = "|"
DATA_SEPARATOR = ","

# Size of a logline.
EVENTLISTSIZE = 7
IEVENTLISTSIZE = 8
# Default logline.
ELIST = range(EVENTLISTSIZE)
IELIST = range(IEVENTLISTSIZE)

DOWN = 'down'
UP = 'up'

# KEY EVENTS
# Message when a key is pressed.
KDOWN = 'key_down'
# Message when a key is released.
KUP = 'key_up'

# MOUSE EVENTS
MOUSE = 'mouse'
MLEFT = 'left'
MMIDDLE = 'middle'
MRIGHT = 'right'
MWHEELUP = 'wheel_up'
MWHEELDOWN = 'wheel_down'

# Set of image formats.
IMG_SET = ['jpg', 'jpeg']
TIMEDATE = '%Y%m%d_%H%M%S_'

# Extension for the target text back up and logfiles.
EXTENSION = '.txt'

WINDOWTITLE = "Sesión de traducción"

# Special keys
KMAP = {32L: "space",
        39L: "apostrophe",  # FIXME
        43L: "plus",
        44L: "comma",
        45L: "minus",  # dash
        46L: "period",  # dot
        48L: "0",
        49L: "1",
        50L: "2",
        51L: "3",
        52L: "4",
        53L: "5",
        54L: "6",
        55L: "7",
        56L: "8",
        57L: "9",
        60L: "less",
        97L: "a",
        98L: "b",
        99L: "c",
        100L: "d",
        101L: "e",
        102L: "f",
        103L: "g",
        104L: "h",
        105L: "i",
        106L: "j",
        107L: "k",
        108L: "l",
        109L: "m",
        110L: "n",
        111L: "o",
        112L: "p",
        113L: "q",
        114L: "r",
        115L: "s",
        116L: "t",
        117L: "u",
        118L: "v",
        119L: "w",
        120L: "x",
        121L: "y",
        122L: "z",
        161L: "exclamdown",
        231L: "ccedilla",
        241L: "ntilde",
        186L: "masculine",
        65027L: "altr",
        65104L: "grave",
        65105L: "acute",
        65288L: "backspace",
        65289L: "tab",  # \t
        65293L: "return",  # \n
        65299L: "pause",
        65300L: "bloq_despl",
        65307L: "escape",
        65360L: "begin",
        65361L: "leftarrow",
        65362L: "uparrow",
        65363L: "rightarrow",
        65364L: "downarrow",
        65365L: "repag",
        65366L: "avpag",
        65367L: "end",
        65377L: "screenshot",
        65379L: "insert",
        65383L: "click",
        65385L: "cancel",  # Cancel the load of a web page
        65407L: "bloq_num",
        65429L: "7",
        65430L: "4",
        65431L: "8",
        65432L: "6",
        65433L: "2",
        65434L: "9",
        65435L: "3",
        65436L: "1",
        65437L: "5",
        65438L: "0",
        65439L: "period",  # dot
        65421L: "return",  # \n
        65450L: "asterisk",  # *
        65451L: "plus",  # +
        65453L: "minus",  # dash
        65455L: "slash",  # /
        65470L: "f1",
        65471L: "f2",
        65472L: "f3",
        65473L: "f4",
        65474L: "f5",
        65475L: "f6",
        65476L: "f7",
        65477L: "f8",
        65478L: "f9",
        65479L: "f10",
        65480L: "f11",
        65481L: "f12",
        65505L: "shiftl",
        65506L: "shiftr",
        65507L: "ctrll",
        65508L: "ctrlr",
        65509L: "mayus",
        65513L: "altl",
        65515L: "windows",
        65516L: "windows",
        65535L: "supr",
        269025048L: "browser",
        269025072L: "favorite",  # Add a web page to favorites
        269025139L: "f5",  # Reload a web page
        269025049L: "mail",  # Opens the mail program by default
        269025053L: "calc",  # Opens the calculator
        269025071L: "suspend",  # Suspends the computer or hibernates?? #FIXME:
        269025074L: "mplayer",  # Opens the music player
        269025045L: "stop",  # Stops the sound if there's music playing
        269025042L: "mute",  # Mute all sounds
        269025046L: "next",  # Next track
        269025047L: "previous",  # Previous track
        269025041L: "vdown",  # Volumne down
        269025043L: "vup",  # Volumen up
        269025044L: "play_pause"  # Play and pause button
        }
