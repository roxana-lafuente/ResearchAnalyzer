# !/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
#
# ResearchAnalyzer: Data Analyzer for ResearchLogger
# Copyright (C) 2016  Roxana Lafuente <roxana.lafuente@gmail.com>
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
from loginfo import LogInfo
import os

path = os.getcwd() + "/example_log/"
# Data from one subject.
# LogInfo needs: - Detailed log file path.
#                - Click images file path.
#                - Timed screenshot file path.
#                - System log file path.
click_fn = path + "click_images/clickimagelogfile_zxysp.txt"
keys_fn = path + "detailed_log/detailedlogfile_zxysp.txt"
screenshoots_fn = path + "timed_screenshots/timedscreenshootlogfile_zxysp.txt"
system_fn = path + "system_log/system_log_zxysp.txt"
li = LogInfo(click_fn,  # Your click data file here
             keys_fn,  # Your detailed log file here
             screenshoots_fn,  # Your timed screenshot log file here
             system_fn)  # Your system log data here
# Print clicks summary info.
print "Unique pressed clicks:", li.get_unique_pressed_clicks()
print
print "In-order pressed clicks:", li.get_all_pressed_clicks()
print
print li.get_click_info()
li.print_click_summary()

# Print keys summary info.
print "Unique pressed keys:", li.get_unique_pressed_keys()
print
print "In-order pressed keys:"
for f in li.get_all_pressed_keys():
    keystroke, event_type, window, window_title = f
    print window, ":\t", window_title, "\t", event_type, "\t", keystroke
for f in li.get_letter_info():
    print f
li.print_key_summary()

# Get the time spent in each window.
print "Time spent in:"
times_by_window = li.get_time_by_active_window()
for k in times_by_window:
    print "\t * '%s' = %s ms" % (k, times_by_window[k])

# Plots the keystroke progression graph.
li.plot_keystroke_progression_graph(1)

# Plots the clicks progression graph.
li.plot_clicks_progression_graph(1)

# Plots a pie chart with the values of the time spent in each window
li.plot_window_distribution_pie_chart()

# Print pauses in interval [0, 5000000]
li.print_pauses(0, 5000000)
li.print_pause_summary(0, 5000000)

fn = path + "timed_screenshots/20161108_195732_460991_screenshot.png"
li.plot_clicks_in_screenshot(fn)
