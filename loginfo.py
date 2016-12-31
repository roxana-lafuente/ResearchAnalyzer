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

import mixed_parser
import click_parser
import key_parser
from common import convert_to_hex
import copy
from termcolor import colored
import re
from pause_info import PauseInfo
import datetime
from constants_analysis import *
from math import sqrt
from collections import defaultdict
import matplotlib.pyplot as plt
from PIL import Image

# Get the absolute path to the test files in the directory variable
from inspect import getsourcefile
from os.path import abspath, dirname
directory = dirname(dirname(abspath(getsourcefile(lambda: 0))))

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(directory + "/ResearchLogger/PyKeylogger-1.2.1")
from constants import *
from text_reconstruction import TextReconstructor


import codecs
from colour import Color


class LogInfo:
    """
    Presents the user with different types of summaries of the recorded logs.
    """

    def __init__(self, clicks_fn, keys_fn, screen_fn, system_fn, finale=None):
        """
        Initializes the needed parsers for the LogInfo class.
        """
        self.clicks_parser = click_parser.ClickParser(clicks_fn)
        self.keys_parser = key_parser.KeyParser(keys_fn)
        self.mixed_parser = mixed_parser.Parser(keys_fn, clicks_fn)
        self.clicks_filename = clicks_fn
        self.keys_filename = keys_fn
        self.screenshot_filename = screen_fn
        self.slog_filename = system_fn
        self.finale = finale
        self._pause_info = PauseInfo(self.mixed_parser)
        self.textReconstructor = TextReconstructor()
        if self.finale is not None:
            # Phases analysis is only available if the finale file is given.
            try:
                self._pi = PhaseInfo(self.mixed_parser, self.slog_filename)
            except IndexError:
                pass

    def get_unique_pressed_clicks(self):
        """
            Returns a set with all the type of clicks that have been pressed
        in the translation session.
        """
        pressed_clicks = set({})
        for click in self.clicks_parser.clicks:
            date, time, pn, user, wid, title, ms, msg, x, y, res, img = click
            click_type, msg = msg.split('_')
            pressed_clicks.add(click_type)
        return pressed_clicks

    def get_all_pressed_clicks(self):
        """
            Returns a list with all the type of clicks and coordinates that
            have been pressed in  the translation sesion.
        """
        pressed_clicks = []
        for click in self.clicks_parser.clicks:
            date, time, pn, user, wid, title, ms, msg, x, y, res, img = click
            click_type, msg = msg.split('_')
            pressed_clicks += [(x, y, res, click_type, msg, pn, title)]
        return pressed_clicks

    def get_click_info_for_visualization(self):
        """
            Given a structure containing the parsed log, it creates a list of
        tuples where each row contains the following information:
            TYPE OF CLICK - TIME PRESS - IMAGE NAME
            PRESS MOUSE X - PRESS MOUSE Y - RELEASE MOUSE X - RELEASE MOUSE Y
        """
        # pn - program name
        # wid - window_id
        # x - coordinate x
        # y - coordinate y
        # ms - millisecond
        # pt - press time
        # rt - release time
        # tt - total time
        # dx - down x
        # ux - up x
        result = []  # List of tuples
        pc = {}  # Pending_clicks
        for click in self.clicks_parser.clicks:
            date, time, pn, user, wid, title, ms, msg, x, y, res, img = click
            ct, msg = msg.split('_')  # click_type and message
            if msg == DOWN:
                if ct not in pc:
                    # Fills the list with the partial information.
                    pc[ct] = [ct, [ms], None, None, [x], [y], None, None]
                else:
                    # More than one down.
                    ct, pt, rt, tt, dx, dx, ux, ux = pc.pop(ct)
                    pc[ct] = [ct, pt + [ms], None, None,
                              dx + [x], dx + [y], None, None]
            else:  # It's an UP msg
                if ct not in pc:
                    msg = "Ha ocurrido un error fatal. "
                    msg += "El log no tiene el formato deseado."
                    print msg
                    exit(1)
                else:
                    ct, pt, rt, tt, dx, dy, ux, uy = pc.pop(ct)
                    result += [(ct, pt, img, dx, dy, x, y, pn + "|" + title)]
        return result

    def get_click_info(self):
        """
            Given a structure containing the parsed log, it creates a list of
        tuples where each row contains the following information:
            TYPE OF CLICK - TIME PRESS - RELEASE TIME - TOTAL PRESS TIME -
            PRESS MOUSE X - PRESS MOUSE Y - RELEASE MOUSE X - RELEASE MOUSE Y
        """
        # pn - program name
        # wid - window_id
        # x - coordinate x
        # y - coordinate y
        # ms - millisecond
        # pt - press time
        # rt - release time
        # tt - total time
        # dx - down x
        # ux - up x
        result = []  # List of tuples
        pc = {}  # Pending_clicks
        for click in self.clicks_parser.clicks:
            date, time, pn, user, wid, title, ms, msg, x, y, res, img = click
            ct, msg = msg.split('_')  # click_type and message
            if msg == DOWN:
                if ct not in pc:
                    # Fills the list with the partial information.
                    pc[ct] = [ct, [ms], None, None, [x], [y], None, None]
                else:
                    # More than one down.
                    ct, pt, rt, tt, dx, dx, ux, ux = pc.pop(ct)
                    pc[ct] = [ct, pt + [ms], None, None,
                              dx + [x], dx + [y], None, None]
            else:  # It's an UP msg
                if ct not in pc:
                    msg = "Ha ocurrido un error fatal. "
                    msg += "El log no tiene el formato deseado."
                    print msg
                    exit(1)
                else:
                    ct, pt, rt, tt, dx, dy, ux, uy = pc.pop(ct)
                    result += [(ct, pt, ms, int(ms) -
                                int(pt[0]), dx, dy, x, y)]
        return result

    def print_click_summary(self):
        """
        Prints a summary of the click activity in the session.
        """
        # ct - click_type
        # pn - program_name
        click_amount = 0
        windows = set([])
        for click in self.get_all_pressed_clicks():
            x, y, resolution, ct, msg, pn, title = click
            if msg == 'down':
                click_amount += 1
            windows.add(pn)
        esp = 0
        var = 0
        for click in self.get_click_info():
            click_type, pt, rt, tt, dx, dy, ux, uy = click
            esp += tt
            var += tt * tt
            print tt
        esp = esp / float(click_amount)
        var = (var / float(click_amount)) - (esp * esp)
        # Prints results.
        print "*** RESUMEN DE CLICKS ***"
        print "Cantidad total de clicks:", colored(click_amount, 'blue')
        print "Ventanas en las cuales se hacen clicks:", list(windows)
        print "Tipos de clicks usados:", list(self.get_unique_pressed_clicks())
        print "Tiempo de presión de click promedio:", colored(esp, 'blue')
        print "Varianza en la presión de click:", colored(var, 'blue')
        print "Desviación estándar en la presión de click:", colored(sqrt(var), 'blue')

    def get_unique_pressed_keys(self):
        """
            Returns a set with all the letters that have been pressed during
        the translation session.
        """
        # pn - program_name
        # wid - windows_id
        # ms - milliseconds
        pressed_keys = set({})
        for key in self.keys_parser.keys:
            # Get attributes from the log line.
            date, time, pn, user, wid, title, ms, key_id, msg, x, y = key
            pressed_keys.add(key_id)
        if '#' in pressed_keys:
            pressed_keys.remove('#')
        return pressed_keys

    def get__milliseconds_delta(self, milliseconds):
        '''
        By getting the minimum timestamp it is then possible
        to infer the relation between the timestamps, where the first
        timestamp will be zero and the other ones after it will
        increase by the time passed in between.
        '''
        if not hasattr(self, 'first_milliseconds_timestamp'):
            self.first_milliseconds_timestamp = \
                int(min(min(self.mixed_parser.clicks, key=lambda x: x[6]), min(
                    self.mixed_parser.keys, key=lambda x: x[6]))[6])
        return milliseconds - self.first_milliseconds_timestamp

    def get_date_from_mixedlog_format(self, click_or_key_log):
        '''
        By using the format from mixedlog, where
        click_or_key_log[0] is the date in the format %Y%M, example 199912
        click_or_key_log[1] is the hour/minute in the format %H%M, 1959
        click_or_key_log[6] is the milliseconds that represent the uptime of the machine
        it is possible to combine them into a complete date
        '''
        from_milliseconds = self.get__milliseconds_delta(
            int(click_or_key_log[6])) / 1000.0
        from_milliseconds = datetime.datetime.fromtimestamp(
            from_milliseconds).second
        datehour = click_or_key_log[0] + ' ' + \
            click_or_key_log[1] + str(from_milliseconds)
        date = datetime.datetime.strptime(datehour, "%Y%m%d %H%M%S")
        return date

    def get_clustered_keys(self, cluster_threshold_in_microseconds=5000000):
        '''
        Given a reasonable threshold the keys are grouped together in clusters,
        forming sentences which can be visualized easily.
        '''
        data = []
        process_name_by_date = {}
        for key_info in self.mixed_parser.keys:

            key = key_info[7]

            msg = key_info[8]
            date = self.get_date_from_mixedlog_format(key_info)
            name = key_info[2] + "|" + key_info[5]
            process_name_by_date[date] = name
            data.append((key, date, name, msg))
        for index, item in enumerate(data):
            # feed the text reconstructor with data
            self.textReconstructor.replay_key_function(
                item[0], item[1], item[3])
        # get the reconstructed text and turn it into an array of keys
        data = []
        for tup in self.textReconstructor.keys_and_time:
            if tup[1]:
                data.append((tup[0], tup[1], process_name_by_date[tup[1]]))
        split_dt = datetime.timedelta(
            microseconds=cluster_threshold_in_microseconds)
        dts = (d1[1] - d0[1] for d0, d1 in zip(data, data[1:]))
        split_at = [i for i, dt in enumerate(dts, 1) if dt >= split_dt]
        groups = [data[i:j] for i, j in zip([0] + split_at, split_at + [None])]
        sentences = []
        for group in groups:
            sentence = ''.join([seq[0] for seq in group])
            start_timestamp = str(group[0][1])
            end_timestamp = str(group[len(group) - 1][1])
            name = group[0][2]
            sentences.append((sentence, start_timestamp, end_timestamp, name))
        self.textReconstructor = TextReconstructor()
        return sentences

    def get_all_pressed_keys(self):
        """
            Returns a list with all the keys that had been pressed with
        corresponding up and downs messages.

            It can contain repeated elements because every key can have several
        downs and at least one up event.
        """
        pressed_keys = []
        for key in self.keys_parser.keys:
            # Get attributes from the log line.
            date, time, pn, user, wid, title, ms, key_id, msg, x, y = key
            key_type, msg = msg.split("_")
            pressed_keys.append((key_id, msg, pn, title))
        return pressed_keys

    def get_letter_info(self):
        """
            Given a structure containing the parsed log, it creates a list of
        tuples where each row contains the following information:
            KEY - TIME PRESS - RELEASE TIME - TOTAL PRESS TIME -
            PRESS MOUSE X - PRESS MOUSE Y - RELEASE MOUSE X - RELEASE MOUSE Y
        """
        # pk - pending_keys
        # pn - program_name
        # kd - key_dict
        result = []  # List of tuples
        # Create keySet
        kd = dict([])
        keywds = []
        for key_struct in self.keys_parser.keys:
            date, time, pn, user, wid, title, ms, key, msg, x, y = key_struct
            keywds += [ms]
            kd[ms] = key_struct
        pk = {}
        for kwd in keywds:
            date, time, pn, user, wid, title, ms, key, msg, x, y = kd[kwd]
            if msg == KDOWN:
                if key not in pk:
                    # Fills the list with the partial information.
                    pk[key] = \
                        [key, [ms], None, None, [x], [y], None, None]
                else:
                    # More than one down.
                    key, pt, rt, tt, dx, dy, ux, uy = pk.pop(key)
                    pk[key] = [key, pt + [ms], None, None,
                               dx + [x], dy + [y], None, None]
            else:  # It's an UP msg
                if key not in pk:
                    msg = "Ha ocurrido un error fatal. "
                    msg += "El log no tiene el formato deseado."
                    print msg
                    exit(1)
                else:
                    key, pt, rt, tt, dx, dy, ux, uy = pk.pop(key)
                    result += [(key, pt, ms, int(ms) -
                                int(pt[0]), dx, dy, x, y)]
        return result

    def _get_combos(self):
        """
        Returns the list of combos that were used in the session.
        """
        combos = []
        # CTRL + KEY combos
        # Eg. CTRL + V, CTRL + C, etc
        combo = []
        combing = False
        found_key = None
        SPECIAL = {'ctrll', 'ctrlr', 'altl', 'altr'}
        for key in self.keys_parser.keys:
            date, time, pn, user, wid, title, ms, keystroke, msg, x, y = key
            if msg == 'key_down' and keystroke in SPECIAL and not combing:
                combo += [keystroke]
                found_key = keystroke
                combing = True
            elif msg == 'key_down' and combing:
                combo += [keystroke]
            elif msg == 'key_up' and combing and keystroke == found_key:
                if len(combo) > 1:
                    combos += [combo]
                combing = False
                found_key = None
                combo = []

        return combos

    def print_key_summary(self):
        """
        Prints a complete summary on the key log file.
        """
        key_amount = 0
        function_keys = set([])
        move_keys = set([])
        erase_keys = set([])
        combos = self._get_combos()
        windows = set([])
        for k in self.keys_parser.keys:
            date, time, pn, user, wid, title, ms, key, msg, x, y = k
            if msg == "key_down":
                key_amount += 1
            windows.add(pn)
            if key in FUNCTION_KEYS:
                function_keys.add(key)
            elif key in ERASE_KEYS:
                erase_keys.add(key)
            elif key in MOVE_KEYS:
                move_keys.add(key)
        esp = 0
        var = 0
        for k in self.get_letter_info():
            key, dt, ut, tt, dx, dy, ux, uy = k
            esp += tt
            var += tt * tt
        esp = esp / float(key_amount)
        var = (var / float(key_amount)) - (esp * esp)
        # Print results
        print "*** RESUMEN DE TECLAS ***"
        print "Cantidad de teclas presionadas:", colored(key_amount, 'blue')
        print "Teclas únicas presionadas:", list(self.get_unique_pressed_keys())
        print "Ventanas donde se esribió:", list(windows)
        print "Tiempo de presión de tecla promedio:", colored(esp, 'blue')
        print "Varianza de presión de tecla:", colored(var, 'blue')
        print "DE de presión de tecla:", colored(sqrt(var), 'blue')
        print "Teclas de función usadas:", list(function_keys)
        print "Patrones de borrado usados:", list(erase_keys)
        print "Teclas de movimiento usadas:", list(move_keys)
        print "Combos de teclas usados:", list(combos)

    def get_orientation_info(self):
        """
        Returns a pair (begin, end) of the time of the orientation phase.
        """
        return self._pi.get_orientation_info()

    def get_drafting_info(self):
        """
        Returns a pair (begin, end) of the time of the drafting phase.
        """
        return self._pi.get_drafting_info()

    def get_revision_info(self):
        """
        Returns a pair (begin, end) of the time of the revision phase.
        """
        return self._pi.get_revision_info()

    def get_total_session_time(self):
        """
        Returns the total session time.
        """
        return self._pi.get_total_session_time()

    def print_phases_summary(self):
        """
        Prints a summary on the translation phases: duration, percentage of the
        sesion, etc.
        """
        print "*** RESUMEN DE FASES ***"
        self._pi.print_orientation_info()
        self._pi.print_drafting_info()
        self._pi.print_revision_info()
        self._pi.print_total_session_info()

    def print_pauses(self, begin, end):
        """
        Prints a summary on the pauses.
        """
        self._pause_info.print_pauses(begin, end)

    def get_time_by_active_window(self):
        """
        By using the knowledge that immediately after a click or a key is down inside a program
        then that program is the active program, then the time between that event and the next
        can be assigned as time used inside that program, the active one.
        Doing this for all of the recorded events gives back the amount of time spent on each
        active program, with no superposition in between them whatsoever.
        """
        time_by_active_window = {}
        time_by_active_window["total"] = 0
        for i in range(len(self.mixed_parser.keys) - 1):
            # Get current keystroke.
            cdate, ctime, cprogram_name, cusername, cwindow_id, cwindow_title, cmiliseconds, ckey, cmsg, cxcoord, cycoord = self.mixed_parser.keys[
                i]
            # Get next keystroke.
            ndate, ntime, nprogram_name, nusername, nwindow_id, nwindow_title, nmiliseconds, nkey, nmsg, nxcoord, nycoord = self.mixed_parser.keys[
                i + 1]

            delta = int(nmiliseconds) - int(cmiliseconds)
            if cprogram_name in time_by_active_window:
                time_by_active_window[cprogram_name] += delta
            else:
                time_by_active_window[cprogram_name] = delta

            time_by_active_window["total"] += delta
        return time_by_active_window

    def plot_window_distribution_pie_chart(self):
        """
        Plots a pie chart of how the windows used in the session.
        """
        # Get data
        win_distrib = self.get_time_by_active_window()
        del win_distrib['total']
        keys = win_distrib.keys()
        values = win_distrib.values()

        # Pick colors
        start_color = Color("#CCE5FF")
        colors = map(convert_to_hex, list(
            start_color.range_to(Color("#003366"), len(keys))))

        # Plot pie chart
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.pie(values,
               autopct='%1.0f%%',
               pctdistance=1.1,
               labeldistance=0.5,
               shadow=True,
               startangle=10,
               colors=colors)
        ax.set_title("Pie chart: Time spent by window")
        plt.legend(keys, loc="best", shadow=True)
        plt.show()

    # def get_pauses_by_phase(self, phase):
    #     """
    #     Returns a list with all the pauses in:
    #     - phase == 1: the orientation phase.
    #     - phase == 2: the drafting phase.
    #     - phase == 3: the revision phase.
    #     """
    #     if phase == 1:
    #         begin, end = self._pi.get_orientation_info()
    #         return self._pause_info.get_pauses(begin, end)
    #     elif phase == 2:
    #         begin, end = self._pi.get_drafting_info()
    #         return self._pause_info.get_pauses(begin, end)
    #     elif phase == 3:
    #         begin, end = self._pi.get_revision_info()
    #         return self._pause_info.get_pauses(begin, end)
    #     else:
    #         return None

    def print_pause_summary(self, begin, end):
        """
        Prints a summary of the pauses in the session.
        """
        return self._pause_info.print_pause_summary(begin, end)

    def plot_keystroke_progression_graph(self, bin_size):
        """
        Plots a keystroke progression graph.
        @bin_size is the bin size in seconds
        """
        last_bin_size = bin_size * 1000  # Convert to milliseconds
        current_bin, current_bin_size = 0, 0
        keystrokes = defaultdict(int)
        current_keystrokes, i = 0, 0
        start = int(self.keys_parser.keys[0][6])  # ms
        while i < len(self.keys_parser.keys):
            d, t, pn, user, wid, title, ms, key_id, msg, x, y = self.keys_parser.keys[
                i]
            ms = int(ms) - start  # force to start from ms 0
            if current_bin_size + ms <= last_bin_size:
                if "down" in msg:
                    current_bin_size += ms
                    current_keystrokes += 1
            else:
                current_bin_size = 0
                if "down" in msg:
                    current_keystrokes += 1
                    current_bin_size += ms
                last_bin_size *= 2
                keystrokes[current_bin] = current_keystrokes
                current_bin += 1
            i += 1
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(keystrokes.keys(), keystrokes.values(), 'r', color='#4682b4')
        ax.plot(keystrokes.keys(), keystrokes.values(), 'o', color='#19457e')
        ax.set_xlabel('# Bins of %s milliseconds' % str(bin_size * 1000))
        ax.set_ylabel('# Keystrokes')
        ax.set_title("Keystroke progression graph")
        ax.plot()
        plt.show()

    def plot_clicks_progression_graph(self, bin_size):
        """
        Plots a clicks progression graph.
        @bin_size is the bin size in seconds
        """
        last_bin_size = bin_size * 1000  # Convert to milliseconds
        current_bin, current_bin_size = 0, 0
        clicks = defaultdict(int)
        current_clicks, i = 0, 0
        start = int(self.clicks_parser.clicks[0][6])  # ms
        while i < len(self.clicks_parser.clicks):
            date, time, pn, user, wid, title, ms, msg, x, y, res, img = self.clicks_parser.clicks[
                i]
            ms = int(ms) - start  # force to start from ms 0
            if current_bin_size + ms <= last_bin_size:
                if "down" in msg:
                    current_bin_size += ms
                    current_clicks += 1
            else:
                current_bin_size = 0
                if "down" in msg:
                    current_clicks += 1
                    current_bin_size += ms
                last_bin_size *= 2
                clicks[current_bin] = current_clicks
                current_bin += 1
            i += 1
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.plot(clicks.keys(), clicks.values(), 'r', color='#4682b4')
        ax.plot(clicks.keys(), clicks.values(), 'o', color='#19457e')
        ax.set_xlabel('# Bins of %s milliseconds' % str(bin_size * 1000))
        ax.set_ylabel('# Clicks pressed')
        ax.set_title("Clicks progression graph")
        plt.show()

    def mark_click(self, x, y, r=0, b=0, g=0):
        """
        @brief      Marks a pixel and neighbors in an image.
        """
        if x - 1 >= 0:
            if y - 1 >= 0:
                self.pixels[x - 1, y - 1] = (r, b, g)
            self.pixels[x - 1, y] = (r, b, g)
            if y + 1 < self.img_height:
                self.pixels[x - 1, y + 1] = (r, b, g)
        if y - 1 >= 0:
            self.pixels[x, y - 1] = (r, b, g)
        self.pixels[x, y] = (r, b, g)
        if y + 1 < self.img_height:
            self.pixels[x, y + 1] = (r, b, g)
        if x + 1 < self.img_width:
            if y - 1 >= 0:
                self.pixels[x + 1, y - 1] = (r, b, g)
            self.pixels[x + 1, y] = (r, b, g)
            if y + 1 < self.img_height:
                self.pixels[x + 1, y + 1] = (r, b, g)

    def plot_clicks_in_screenshot(self, screenshot):
        """
        @brief      Marks in a screenshot where clicks were made.

        @param      screenshot  The screenshot path
        """
        img = Image.open(screenshot)
        self.pixels = img.load()
        self.img_width = img.width
        self.img_height = img.height
        # Get clicks (down only)
        clicks = self.get_click_info()
        # Define color
        r, g, b = 40, 205, 106
        # For each click, mark the surrounding area
        for click in clicks:
            _, _, _, _, _, _, x, y = click
            self.mark_click(int(x), int(y), r, g, b)
        img.show()
