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
import copy
from termcolor import colored
import re
import datetime
from constants_analysis import *
from math import sqrt

# Get the absolute path to the test files in the directory variable
from inspect import getsourcefile
from os.path import abspath, dirname
directory = dirname(dirname(abspath(getsourcefile(lambda: 0))))

import sys
sys.path.append(directory + "/ResearchLogger/PyKeylogger-1.2.1")
from constants import *

import codecs


class LogInfo:
    """
    Presents the user with different types of summaries of the recorded logs.
    """
    def __init__(self, clicks_filename, keys_filename, slog_filename):
        """
        Initializes the needed parsers for the LogInfo class.
        """
        self.clicks_parser = click_parser.ClickParser(clicks_filename)
        self.keys_parser = key_parser.KeyParser(keys_filename)
        self.mixed_parser = mixed_parser.Parser(keys_filename, clicks_filename)
        self.clicks_filename = clicks_filename
        self.keys_filename = keys_filename
        self.slog_filename = slog_filename
        try:
            self._pi = PhaseInfo(self.mixed_parser, self.slog_filename)
            self._pause_info = PauseInfo(self.mixed_parser)
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
                    pc[ct] = [ct, pt+[ms], None, None, dx+[x], dx+[y], None, None]
            else:  # It's an UP msg
                if ct not in pc:
                    msg = "Ha ocurrido un error fatal. "
                    msg += "El log no tiene el formato deseado."
                    print msg
                    exit(1)
                else:
                    ct, pt, rt, tt, dx, dy, ux, uy = pc.pop(ct)
                    result += [(ct, pt, ms, int(ms)-int(pt[0]), dx, dy, x, y)]
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
        var = (var/float(click_amount))-(esp*esp)
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
                    pk[key] = [key, pt+[ms], None, None, dx+[x], dy+[y], None, None]
            else:  # It's an UP msg
                if key not in pk:
                    msg = "Ha ocurrido un error fatal. "
                    msg += "El log no tiene el formato deseado."
                    print msg
                    exit(1)
                else:
                    key, pt, rt, tt, dx, dy, ux, uy = pk.pop(key)
                    result += [(key, pt, ms, int(ms)-int(pt[0]), dx, dy, x, y)]
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

    def print_pauses(self):
        """
        Prints a summary on the pauses.
        """
        self._pause_info.print_pauses(0, self._pi.greatest_time)

    def get_pauses(self, phase=0):
        """
        Returns a list with all the pauses in:
        - phase == 0: the session.
        - phase == 1: the orientation phase.
        - phase == 2: the drafting phase.
        - phase == 3: the revision phase.
        """
        if phase == 0:
            return self._pause_info.get_pauses(0, self._pi.greatest_time)
        elif phase == 1:
            begin, end = self._pi.get_orientation_info()
            return self._pause_info.get_pauses(begin, end)
        elif phase == 2:
            begin, end = self._pi.get_drafting_info()
            return self._pause_info.get_pauses(begin, end)
        elif phase == 3:
            begin, end = self._pi.get_revision_info()
            return self._pause_info.get_pauses(begin, end)
        else:
            return None

    def print_pause_summary(self):
        """
        Prints a summary of the pauses in the session.
        """
        return self._pause_info.print_pause_summary(0, self._pi.greatest_time)


class PhaseInfo:
    """
    Given a corpus with # as the marker for the end of drafting phases.
    This class determines info about the translation phases.
    """

    def __init__(self, mp, slog_filename):
        """
        Initializes the PhaseInfo class with the mixed parser and the system log path.
        """
        self.mixed_parser = copy.copy(mp)
        self.slog_filename = slog_filename
        self._set_phases()

    def _set_phases(self):
        """
        Sets the needed values to calculate the translation phases.
        """
        # Get parser.
        self.clicks = self.mixed_parser.clicks
        self.keys = self.mixed_parser.keys
        # tsparser = mixed_parser.Parser(dfile, cfile, TS)
        # keys = copy.copy(tsparser.keys)
        # Get Clicks.
        self.openClicks = []
        for click in self.clicks:
            if 'Abrir' in click:
                self.openClicks += [click]

        # Planning (Start)
        self.ostime = int(self.openClicks[-1][6])

        # Drafting (End)
        self.detime = 0
        try:
            for k in self.keys:
                match = re.findall(r'[\S]*#', " " + ",".join(k))
                if match != []:
                    self.detime = int(match[0].split(",")[1])
                    break
        except:
            pass

        # Revision (End)
        # try:
        system = open(self.slog_filename, 'r').read()
        self.rostime = re.findall(r'[\S]* [\S]* [\S]* [\S]*       [\S]*      [\S]*    [\S]*    [\S]* [\S]* [\S]* [\S]*\n[\S]* [\S]* [\S]*\n[\S]* [\S]* [\S]* [\S]*\n[\S]* [\S]* [\S]*\n[\S]* [\S]*\n[\S]* [\S]*%s' % self.ostime, system)[0].split(",")[0]
        self.rretime = re.findall(r'END: [\S]*', system)[0].split(" ")[1]
        self.rostime = datetime.datetime.strptime(self.rostime, "%H:%M:%S")
        self.rretime = datetime.datetime.strptime(self.rretime, "%H%M%S")
        self.ttime = self.rretime - self.rostime
        self.ttime = str(self.ttime).split(":")
        self.ftime = self.ostime + (int(self.ttime[1]) * 60 + int(self.ttime[2])) * 1000
        self.ttime = (int(self.ttime[1]) * 60 + int(self.ttime[2])) * 1000
        self.retime = self.ftime - self.detime
        self.retime = self.ftime
        self.rstime = self.detime
        self.rtime = self.retime - self.rstime
        # Greatest time seen
        self.greatest_time = self.retime

        # Planning (End)
        self.oetime = int(self.keys[0][6])
        self.otime = self.oetime-self.ostime

        # Drafting (Start)
        self.dstime = self.oetime

        # Revision (Start)
        self.rstime = self.detime
        # Drafting (Show Results)
        self.dtime = self.detime - self.dstime

    def print_orientation_info(self):
        """
        Prints the info on the Planning phase.
        """
        print "*** ORIENTACIÓN ***"
        print "Tiempo de inicio:", colored(self.ostime, 'cyan')
        print "Tiempo de finalización:", colored(self.oetime, 'cyan')
        print "Duración:", colored(self.otime, 'cyan'), "ms =",
        print colored(self.otime/float(1000), 'cyan'), "sec,"
        try:
            print "Porcentaje de la sesión dedicado a la fase de orientación:",
            print colored((self.otime/float(self.ttime))*100, 'cyan'), "%"
        except NameError:
            # st - session time
            self.st = max(int(self.keys[-1][6]), int(self.openClicks[-1][6]))
            self.st -= int(self.openClicks[-2][6])
            print "Porcentaje de la sesión dedicado a la fase de orientación:",
            print colored((self.otime/float(self.st))*100, 'cyan'), "%"

    def print_drafting_info(self):
        """
        Prints the info on the Drafting phase.
        """
        print "*** ELABORACIÓN DE BORRADOR ***"
        print "Tiempo de inicio:", colored(self.dstime, "cyan")
        print "Tiempo de finalización:", colored(self.detime, "cyan")
        print "Duración:", colored(self.dtime, "cyan"), "ms,",
        print colored(self.dtime/float(1000), "cyan"), "sec,"
        try:
            print "Porcentaje de la sesión dedicado a la fase de elaboración",
            print "de borrador:",
            print colored((self.dtime/float(self.ttime))*100, 'cyan'), "%"
        except NameError:
            self.st = max(int(self.keys[-1][6]), int(self.openClicks[-1][6]))
            self.st -= int(self.openClicks[-2][6])
            print "Porcentaje de la sesión dedicado a la fase de elaboración",
            print "de borrador:",
            print colored((self.dtime/float(self.stime))*100, "cyan"), "%"

    def print_revision_info(self):
        """
        Prints the info on the Revision phase.
        """
        print "*** RESUMEN ***"
        print "Tiempo de inicio:", colored(self.rstime, "cyan")
        print "Tiempo de finalización:", colored(self.retime, 'cyan')
        print "Duración:", colored(self.rtime, 'cyan'), "ms, =",
        print colored(self.rtime/float(1000), 'cyan'), "sec,"
        try:
            print "Porcentaje de la sesión dedicado a la fase de revisión:",
            print colored((self.rtime/float(self.ttime))*100, 'cyan'), "%"
        except NameError:
            self.st = max(int(self.keys[-1][6]), int(self.openClicks[-1][6]))
            self.st -= int(self.openClicks[-2][6])
            print (self.rtime/float(self.st))*100, "%"

    def print_total_session_info(self):
        """
        Prints the general info on the session.
        """
        print "*** SESIÓN ***"
        try:
            print "Tiempo total:", colored(self.ttime, 'cyan'), "ms =",
            print colored(self.ttime/float(1000), 'cyan'), "sec =",
            print colored(self.ttime/float(1000*60), 'cyan'), "min"
        except NameError:
            self.st = max(int(self.keys[-1][6]), int(self.openClicks[-1][6]))
            self.st -= int(self.openClicks[-2][6])
            print "Tiempo total:", colored(self.stime, "cyan"), "ms =",
            print colored(self.stime/float(1000), 'cyan'), "sec =",
            print colored(self.stime/float(1000*60), 'cyan'), "min"

    def get_orientation_info(self):
        """
        Returns a pair with the start time and end time of the orientation
        phase in milliseconds.
        """
        return (self.ostime, self.oetime)

    def get_drafting_info(self):
        """
        Returns a pair with the start time and end time of the drafting phase
        in milliseconds.
        """
        return (self.dstime, self.detime)

    def get_revision_info(self):
        """
        Returns a pair with the start time and end time of the revision phase
        in milliseconds.
        """
        return (self.rstime, self.retime)

    def get_total_session_time(self):
        """
        Returns the total time of the session.
        """
        return self.ttime


class PauseInfo:
    """
    Class that shows summaries on pauses from a given log.
    """
    def __init__(self, mixed_parser):
        """
        Defines the needed times pauses for the PauseInfo class.
        """
        self._mixed_parser = mixed_parser

    def _is_short_pause(self, pause):
        """
        Determines if a pause is a short one.
        - pause is in milliseconds
        - a short pause is between 2 and 6 seconds
        """
        return 2000 <= pause and pause < 6000

    def _is_medium_pause(self, pause):
        """
        Determines if a pause is a medium one.
        - pause is in milliseconds
        - a medium pause is between 6 and 60 seconds
        """
        return 6000 <= pause and pause < 60000

    def _is_big_pause(self, pause):
        """
        Determines if a pause is a big one.
        - pause is in milliseconds
        - a big pause is greater than 60 seconds
        """
        return pause >= 60000

    def get_pauses(self, begin, end):
        """
        Given an interval in which pauses should be look for.
        It returns the duration of the pauses and the millisecond in which they
        started.
        """
        pauses = []
        for i in range(len(self._mixed_parser.keys)-1):
            # Get current keystroke.
            cdate, ctime, cprogram_name, cusername, cwindow_id, cwindow_title, cmiliseconds, ckey, cmsg, cxcoord, cycoord = self._mixed_parser.keys[i]
            # Get next keystroke.
            ndate, ntime, nprogram_name, nusername, nwindow_id, nwindow_title, nmiliseconds, nkey, nmsg, nxcoord, nycoord = self._mixed_parser.keys[i+1]
            if begin <= min(int(nmiliseconds), int(cmiliseconds)) and max(int(nmiliseconds), int(cmiliseconds)) <= end:
                pauses += [(int(cmiliseconds), int(nmiliseconds)-int(cmiliseconds))]
        return pauses

    def print_pauses(self, begin, end):
        """
        Prints a summary of the short, medium and big pauses in the session.
        All pauses that do not fall in these categories are ignored.
        """
        pauses = self.get_pauses(begin, end)
        i = 0
        for pause in pauses:
            i += 1
            if self._is_short_pause(pause):
                print "Pausa #", i, ":", colored(str(pause), "green"), "ms"
            elif self._is_medium_pause(pause):
                print "Pausa #", i, ":", colored(str(pause), "yellow"), "ms"
            elif self._is_big_pause(pause):
                # It's a big pause
                print "Pausa #", i, ":", colored(str(pause), "red"), "ms"

    def print_pause_summary(self, begin, end):
        pauses = self.get_pauses(begin, end)
        # Set how many pauses occurred and which types.
        short_pauses, medium_pauses, big_pauses = 0, 0, 0
        sum_pauses = 0
        var_pauses = 0
        for pause in pauses:
            start, duration = pause
            sum_pauses += duration
            var_pauses += duration * duration
            short_pauses += self._is_short_pause(duration)
            medium_pauses += self._is_medium_pause(duration)
            big_pauses += self._is_big_pause(duration)
        # Calculates the variance.
        esp_pauses = sum_pauses/float(len(pauses))
        var_pauses = (1/float(len(pauses)) * var_pauses) - (esp_pauses * esp_pauses)
        other_pauses = len(pauses)-short_pauses-medium_pauses-big_pauses
        # Print results.
        print "*** RESUMEN DE PAUSAS ***"
        print "Cantidad total de pausas en el intervalo [", begin, "ms ,", end, "ms ]:", colored(len(pauses), "blue")
        print "Cantidad de pausas cortas:", colored(short_pauses, "blue"), "-", colored(short_pauses/float(len(pauses)), "cyan"), "%"
        print "Cantidad de pausas medianas:", colored(medium_pauses, "blue"), "-", colored(medium_pauses/float(len(pauses)), "cyan"), "%"
        print "Cantidad de pausas largas:", colored(big_pauses, "blue"), "-", colored(big_pauses/float(len(pauses)), "cyan"), "%"
        print "Cantidad de pausas no significativas:", colored(other_pauses, "blue"), "-", colored(other_pauses/float(len(pauses)), "cyan"), "%"
        print "Tiempo de pausa promedio:", colored(esp_pauses, "blue")
        print "Varianza en el tiempo de las pausas:", colored(var_pauses, "blue")