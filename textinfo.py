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
from nltk import pos_tag, word_tokenize, FreqDist
from constants import LINE_SEPARATOR
from collections import defaultdict


class TextInfo:
    """
    @brief      Presents the user with different types of summaries of the
                final document.
    """

    def __init__(self, finale=None):
        """
        @brief      Reads the finale document given and saves the necessary
                    info for future analysis.
        """
        self.finale = finale
        with open(finale, 'r') as f:
            self.raw = f.readlines()[-1].replace('\n', '')
            self.words = self.raw.split(LINE_SEPARATOR)
        self.tokenized_text = word_tokenize(self.raw)

    def get_words_by_part_of_speech(self):
        """
        @brief      Groups words by part_of_speech.

        @param      self  The object

        @return     The words by part of speech.
        """
        grouped_by_part_of_speech_words = defaultdict(list)

        for word, part_of_speech in pos_tag(self.tokenized_text):
            grouped_by_part_of_speech_words[part_of_speech] += [word]

        return dict(grouped_by_part_of_speech_words)

    def get_sentences(self):
        """
        @brief      Gets the sentences from the finale file.

        @param      self  The object

        @return     The sentences.
        """
        sentences = []
        sentences = self.raw.split(".")[:-1]
        for i, sentence in enumerate(sentences):
            sentences[i] = sentence.lstrip()
        return sentences

    def get_n_most_frequent_words(self, n):
        """
        @brief      Get n most frequent words.

        @param      self  The object
        param       n     The desired number of most frequent words
        """
        assert(isinstance(n, int))
        fd = FreqDist(self.tokenized_text)
        return fd.keys()

    def plot_frequency_distribution(self, n):
        """
        @brief      Plots a frequency distribution plot.

        @param      self  The object
        param       n     The desired number of most frequent words
        """
        assert(isinstance(n, int))
        fd = FreqDist(self.tokenized_text)
        fd.plot(n, cumulative=True)
