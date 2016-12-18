# !/usr/bin/env python
# -*- coding: utf-8 -*-

from constants import *

class TextReconstructor:

    def __init__(self):
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

    def append_to_screen(self, msg):
        self.screen += msg
        self.ycursor += len(msg)
