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
from nltk import pos_tag, word_tokenize
from constants import LINE_SEPARATOR
from collections import defaultdict


class TextInfo:
    """
    Presents the user with different types of summaries of the final document.
    """
    def __init__(self, finale=None):
        """
        Initializes the needed parsers for the LogInfo class.
        """
        self.finale = finale
        with open(finale, 'r') as f:
            self.raw = f.readlines()[-1].replace('\n', '')
            self.words = self.raw.split(LINE_SEPARATOR)

    def get_words_by_part_of_speech(self):
        grouped_by_part_of_speech_words = defaultdict(list)
        words = word_tokenize(self.raw)

        for word, part_of_speech in pos_tag(words):
            grouped_by_part_of_speech_words[part_of_speech] += [word]

        return dict(grouped_by_part_of_speech_words)

    def get_sentences(self):
        sentences = []
        sentences = self.raw.split(".")[:-1]
        for i, sentence in enumerate(sentences):
            sentences[i] = sentence.lstrip()
        return sentences
