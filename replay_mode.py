# !/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import os
from constants import *
from mixed_parser import Parser
from text_reconstruction import TextReconstructor


def define_up_down_behaviour(msg, upb, downb):
    if msg.endswith("down"):
        return downb
    else:
        return upb


class ReplayMode:

    def __init__(self, keys_filename, clicks_filename, searchpattern=''):
        self.parser = Parser(keys_filename, clicks_filename, searchpattern)
        self.textReconstructor = TextReconstructor()

    def print_status(self):
        print "self.textReconstructor.xcursor:", self.textReconstructor.xcursor
        print "self.textReconstructor.ycursor:", self.textReconstructor.ycursor
        print "self.textReconstructor.is_shift_pressed:", self.textReconstructor.is_shift_pressed
        print "self.textReconstructor.is_ctrl_pressed:", self.textReconstructor.is_ctrl_pressed
        print "self.textReconstructor.is_alt_pressed:", self.textReconstructor.is_alt_pressed
        print "self.textReconstructor.is_bloqmayus_pressed:", self.textReconstructor.is_bloqmayus_pressed

    def replay_key_function(self, time, key, msg, delay=0):
        """
            Given a key, this function actually acts like the function of the
            key.
        """
        # FIXME: self.textReconstructor.screen debería ser una lista de listas de strings (una matriz)
        if(len(key) == 1):
            # It's an ascii key.
            if (self.textReconstructor.is_shift_pressed or self.textReconstructor.is_bloqmayus_pressed):
                key = key.upper()
            # We consider the key if it is being pressed (down).
            self.textReconstructor.append_to_screen(define_up_down_behaviour(msg, "", key))
        else:
            # It's a function key.
#            print "evaluating.." , "self.replay_" + str(key) + "(" + str(msg) + ")"
            eval("self.textReconstructor.replay_" + str(key) + "(msg)")

    def replay_quick_mode(self):
        for k in self.parser.merged:
            try:
                date, time, program_name, username, window_id, window_title, ms, key, msg, x, y = k
                self.replay_key_function(ms, key, msg)
            except ValueError:
                date, real_time, program_name, username, window_id, window_title, ms, msg, x, y, resolution, img_name = k
                self.replay_key_function(ms, msg.split("_")[0], msg)

    def print_screen(self):
        print self.textReconstructor.screen

    def get_screen(self):
        return self.textReconstructor.screen

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
