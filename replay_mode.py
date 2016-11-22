# !/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import os
from constants import *
from mixed_parser import Parser


def define_up_down_behaviour(msg, upb, downb):
    if msg.endswith("down"):
        return downb
    else:
        return upb


class ReplayMode:

    def __init__(self, keys_filename, clicks_filename, searchpattern=''):
        self.parser = Parser(keys_filename, clicks_filename, searchpattern)
        self.screen = ""
        # We act as if the text was a matrix of characters.
        self.xcursor = 0
        self.ycursor = 0
        # Gets a registry of which keys are pressed that may change default
        # behaviour.
        self.is_shift_pressed = False
        self.is_ctrl_pressed = False
        self.is_alt_pressed = False
        self.is_bloqmayus_pressed = False

    def print_status(self):
        print "self.xcursor:", self.xcursor
        print "self.ycursor:", self.ycursor
        print "self.is_shift_pressed:", self.is_shift_pressed
        print "self.is_ctrl_pressed:", self.is_ctrl_pressed
        print "self.is_alt_pressed:", self.is_alt_pressed
        print "self.is_bloqmayus_pressed:", self.is_bloqmayus_pressed

    def replay_altr(self, msg):
        if msg == KDOWN:
            pass

    def replay_space(self, msg):
        if msg == KDOWN:
            self.screen += " "
            self.ycursor += 1

    def replay_apostrophe(self, msg):
        if msg == KDOWN:
            self.screen += "'"
            self.ycursor += 1

    def replay_plus(self, msg):
        if msg == KDOWN:
            self.screen += "+"
            self.ycursor += 1

    def replay_comma(self, msg):
        if msg == KDOWN:
            self.screen += ","
            self.ycursor += 1

    def replay_minus(self, msg):
        if msg == KDOWN:
            self.screen += "-"
            self.ycursor += 1

    def replay_period(self, msg):
        if msg == KDOWN:
            self.screen += "."
            self.ycursor += 1

    def replay_less(self, msg):
        if msg == KDOWN:
            self.screen += "<"
            self.ycursor += 1

    def replay_grave(self, msg):
        if msg == KDOWN:
            pass

    def replay_acute(self, msg):
        if msg == KDOWN:
            pass

    def replay_exclamdown(self, msg):
        if msg == KDOWN:
            self.screen += "!"
            self.ycursor += 1

    def replay_masculine(self, msg):
        if msg == KDOWN:
            self.screen += "º"
            self.ycursor += 1

    def replay_ccedilla(self, msg):
        if msg == KDOWN:
            self.screen += "ç"
            self.ycursor += 1

    def replay_ntilde(self, msg):
        if msg == KDOWN:
            self.screen += "ñ"
            self.ycursor += 1

    def replay_backspace(self, msg):
        if msg == KDOWN:
            self.screen = self.screen[0:self.ycursor-1]+self.screen[self.ycursor:len(self.screen)]# self.screen[0:len(self.screen) - 1]
            self.ycursor -= 1

    def replay_tab(self, msg):
        if msg == KDOWN:
            self.screen += "\t"

    def replay_return(self, msg):
        if msg == KDOWN:
            self.screen += "\n"
            self.xcursor += 1

    def replay_bloq_despl(self, msg):
        if msg == KDOWN:
            pass

    def replay_escape(self, msg):
        if msg == KDOWN:
            pass

    def replay_begin(self, msg):
        if msg == KDOWN:
            pass  # cursor en posicion 0 de la linea actual

    def replay_leftarrow(self, msg):
        if msg == KDOWN:
            self.ycursor -= 1

    def replay_uparrow(self, msg):
        if msg == KDOWN:
            self.screen += "#"
        #     self.xcursor += 1

    def replay_rightarrow(self, msg):
        if msg == KDOWN:
            self.ycursor += 1

    def replay_downarrow(self, msg):
        if msg == KDOWN:
            self.screen += "+"
        #     self.xcursor -= 1

    def replay_repag(self, msg):
        if msg == KDOWN:
            pass

    def replay_avpag(self, msg):
        if msg == KDOWN:
            pass

    def replay_end(self, msg):
        if msg == KDOWN:
            self.ycursor = len(self.screen) - 1

    def replay_screenshot(self, msg):
        if msg == KDOWN:
            pass

    def replay_insert(self, msg):
        if msg == KDOWN:
            pass

    def replay_left(self, msg):
        print "click"
        if msg == KDOWN:
            pass

    def replay_middle(self, msg):
        print "click"
        if msg == KDOWN:
            pass

    def replay_right(self, msg):
        print "click"
        if msg == KDOWN:
            pass

    def replay_cancel(self, msg):
        if msg == KDOWN:
            pass

    def replay_bloq_num(self, msg):
        if msg == KDOWN:
            pass

    def replay_asterisk(self, msg):
        if msg == KDOWN:
            pass

    def replay_slash(self, msg):
        if msg == KDOWN:
            pass

    def replay_f1(self, msg):
        if msg == KDOWN:
            pass

    def replay_f2(self, msg):
        if msg == KDOWN:
            pass

    def replay_f3(self, msg):
        if msg == KDOWN:
            pass

    def replay_f4(self, msg):
        if msg == KDOWN:
            pass

    def replay_f5(self, msg):
        if msg == KDOWN:
            pass

    def replay_f6(self, msg):
        if msg == KDOWN:
            pass

    def replay_f7(self, msg):
        if msg == KDOWN:
            pass

    def replay_f8(self, msg):
        if msg == KDOWN:
            pass

    def replay_f9(self, msg):
        if msg == KDOWN:
            pass

    def replay_f10(self, msg):
        if msg == KDOWN:
            pass

    def replay_f11(self, msg):
        if msg == KDOWN:
            pass

    def replay_f12(self, msg):
        if msg == KDOWN:
            pass

    def replay_shiftl(self, msg):
        self.is_shift_pressed = not self.is_shift_pressed

    def replay_shiftr(self, msg):
        self.is_shift_pressed = not self.is_shift_pressed

    def replay_ctrll(self, msg):
        if msg == KDOWN:
            pass

    def replay_ctrlr(self, msg):
        if msg == KDOWN:
            pass

    def replay_mayus(self, msg):
        if msg == KDOWN:
            self.is_bloqmayus_pressed = not self.is_bloqmayus_pressed

    def replay_altl(self, msg):
        if msg == KDOWN:
            pass

    def replay_windows(self, msg):
        if msg == KDOWN:
            pass

    def replay_supr(self, msg):
        if msg == KDOWN:
            self.screen = self.screen[0:self.ycursor]+self.screen[self.ycursor+1:len(self.screen)] #self.screen[len(self.screen) - 1]

    def replay_key_function(self, time, key, msg, delay=0):
        """
            Given a key, this function actually acts like the function of the
            key.
        """
        # FIXME: self.screen debería ser una lista de listas de strings (una matriz)
        if(len(key) == 1):
            # It's an ascii key.
            if (self.is_shift_pressed or self.is_bloqmayus_pressed):
                key = key.upper()
            # We consider the key iff it is being pressed (down).
            if msg == KDOWN:
                self.ycursor += 1
            self.screen += define_up_down_behaviour(msg, "", key)
        else:
            # It's a function key.
#            print "evaluating.." , "self.replay_" + str(key) + "(" + str(msg) + ")"
            eval("self.replay_" + str(key) + "(msg)")

    def replay_quick_mode(self):
        self.cursor = len(self.screen)
        for k in self.parser.merged:
            try:
                date, time, program_name, username, window_id, window_title, ms, key, msg, x, y = k
                self.replay_key_function(ms, key, msg)
            except ValueError:
                date, real_time, program_name, username, window_id, window_title, ms, msg, x, y, resolution, img_name = k
                self.replay_key_function(ms, msg.split("_")[0], msg)

    def print_screen(self):
        print self.screen

    def get_screen(self):
        return self.screen

    def replay_mode(self):
        """
            Replays the translation session from the logfile with advanced
        options.
        """
        pass

# Main program
keys_filename = 'example_log/detailed_log/detailedlogfile_zxysp.txt'
clicks_filename = 'example_log/click_images/clickimagelogfile_zxysp.txt'
finale_filename = 'example_log/example_log_target_text.txt'

with open(finale_filename, "r") as f:
    fwords = f.read().split("\n")[3].split(" ")

r = ReplayMode(keys_filename, clicks_filename, 'Sesión de traducción')
r.replay_quick_mode()
print r.get_screen()
rwords = r.get_screen().split(" ")[:-1]
tmp = rwords[-1].split(".")
# print tmp
# rwords[-1], missing_changes = tmp[0], tmp[1]
for i in range(len(rwords)):
    print rwords[i], fwords[i]
print rwords
revision_changes = []
for word in rwords[::-1]:
	if "." in word:
		revision_changes += word.split(".")[1:]
		break
	else:
		revision_changes += [word]
print revision_changes[::-1]