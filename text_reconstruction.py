# !/usr/bin/env python
# -*- coding: utf-8 -*-

from constants import *


class TextReconstructor:

    def __init__(self):
        self.screen = ""
        # We act as if the text was a matrix of characters.
        self.xcursor = 0
        self.ycursor = 0
        # keys and time is an array of tuples
        # with the pressed key as [0]
        # and the complete date it was pressed as [1]
        self.keys_and_time = []
        # Gets a registry of which keys are pressed that may change default
        # behaviour.
        self.is_shift_pressed = False
        self.is_ctrl_pressed = False
        self.is_alt_pressed = False
        self.is_bloqmayus_pressed = False

    def replay_key_function(self, key, time=0, msg="key_down", delay=0):
        """
            Given a key, this function actually acts like the function of the
            key.
        """
        # FIXME: self.textReconstructor.screen debería ser una lista de listas
        # de strings (una matriz)
        if(len(key) == 1):
            # It's an ascii key.
            if (self.is_shift_pressed or self.is_bloqmayus_pressed):
                key = key.upper()
            # We consider the key if it is being pressed (down).
            self.append_to_screen(
                self.define_up_down_behaviour(msg, "", key), time)
        else:
            # It's a function key.
            eval("self.replay_" + str(key) + "(msg, time)")

    def replay_altr(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_space(self, msg, time=0):
        if msg == KDOWN:
            self.append_to_screen(" ", time)

    def replay_apostrophe(self, msg, time=0):
        if msg == KDOWN:
            self.append_to_screen("'", time)

    def replay_plus(self, msg, time=0):
        if msg == KDOWN:
            self.append_to_screen("+", time)

    def replay_comma(self, msg, time=0):
        if msg == KDOWN:
            self.append_to_screen(",", time)

    def replay_minus(self, msg, time=0):
        if msg == KDOWN:
            self.append_to_screen("-", time)

    def replay_period(self, msg, time=0):
        if msg == KDOWN:
            self.append_to_screen(".", time)

    def replay_less(self, msg, time=0):
        if msg == KDOWN:
            self.append_to_screen("<", time)

    def replay_grave(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_acute(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_exclamdown(self, msg, time=0):
        if msg == KDOWN:
            self.append_to_screen("!", time)

    def replay_masculine(self, msg, time=0):
        if msg == KDOWN:
            self.append_to_screen("º", time)

    def replay_ccedilla(self, msg, time=0):
        if msg == KDOWN:
            self.append_to_screen("ç", time)

    def replay_ntilde(self, msg, time=0):
        if msg == KDOWN:
            self.append_to_screen("ñ", time)

    def replay_backspace(self, msg, time=0):
        if msg == KDOWN:
            # self.screen[0:len(self.screen) - 1]
            self.screen = self.screen[0:self.ycursor - 1] + \
                self.screen[self.ycursor:len(self.screen)]
            self.keys_and_time = self.keys_and_time[
                0:self.ycursor - 1] + self.keys_and_time[self.ycursor:len(self.keys_and_time)]
            self.ycursor -= 1

    def replay_tab(self, msg, time=0):
        if msg == KDOWN:
            self.append_to_screen("\t", time)

    def replay_return(self, msg, time=0):
        if msg == KDOWN:
            self.append_to_screen("\n", time)

    def replay_bloq_despl(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_escape(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_begin(self, msg, time=0):
        if msg == KDOWN:
            pass  # cursor en posicion 0 de la linea actual

    def replay_leftarrow(self, msg, time=0):
        if msg == KDOWN:
            self.ycursor -= 1

    def replay_uparrow(self, msg, time=0):
        if msg == KDOWN:
            self.screen += "#"
        #     self.xcursor += 1

    def replay_rightarrow(self, msg, time=0):
        if msg == KDOWN:
            self.ycursor += 1

    def replay_downarrow(self, msg, time=0):
        if msg == KDOWN:
            self.screen += "+"
        #     self.xcursor -= 1

    def replay_repag(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_avpag(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_end(self, msg, time=0):
        if msg == KDOWN:
            self.ycursor = len(self.screen) - 1

    def replay_screenshot(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_insert(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_left(self, msg, time=0):
        print "click"
        if msg == KDOWN:
            pass

    def replay_middle(self, msg, time=0):
        print "click"
        if msg == KDOWN:
            pass

    def replay_right(self, msg, time=0):
        print "click"
        if msg == KDOWN:
            pass

    def replay_cancel(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_bloq_num(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_asterisk(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_slash(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_f1(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_f2(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_f3(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_f4(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_f5(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_f6(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_f7(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_f8(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_f9(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_f10(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_f11(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_f12(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_shiftl(self, msg, time=0):
        self.is_shift_pressed = not self.is_shift_pressed

    def replay_shiftr(self, msg, time=0):
        self.is_shift_pressed = not self.is_shift_pressed

    def replay_ctrll(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_ctrlr(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_mayus(self, msg, time=0):
        if msg == KDOWN:
            self.is_bloqmayus_pressed = not self.is_bloqmayus_pressed

    def replay_altl(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_windows(self, msg, time=0):
        if msg == KDOWN:
            pass

    def replay_supr(self, msg, time=0):
        if msg == KDOWN:
            # self.screen[len(self.screen) - 1]
            self.screen = self.screen[0:self.ycursor] + \
                self.screen[self.ycursor + 1:len(self.screen)]

    def define_up_down_behaviour(self, msg, upb, downb):
        if msg.endswith("down"):
            return downb
        else:
            return upb

    def append_to_screen(self, msg, time=0):
        self.screen += msg
        self.keys_and_time.insert(self.ycursor, (msg, time))
        self.ycursor += len(msg)
