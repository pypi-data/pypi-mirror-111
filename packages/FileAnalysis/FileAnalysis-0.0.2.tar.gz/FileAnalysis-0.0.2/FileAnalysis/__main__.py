#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This package analyze emergence of characters in file (for statistics decryption). """

###################
#    This package analyze emergence of characters in file (for statistics decryption).
#    Copyright (C) 2021  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

try:
    from FileAnalysis import main as analyze
except ImportError:
    from .FileAnalysis import main as analyze

analyze()
