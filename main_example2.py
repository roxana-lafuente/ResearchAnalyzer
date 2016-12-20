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
from textinfo import TextInfo
import os

path = os.getcwd() + "/example_log/"

ti = TextInfo(path + "example_log_target_text.txt")

print ti.get_words_by_part_of_speech()

print ti.get_sentences()

ti.plot_frequency_distribution(50)

print ti.get_n_most_frequent_words(20)
