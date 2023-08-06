#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This file analyze emergence of characters in file (to decrypt with statistics). """

###################
#    This file analyze emergence of characters in file (for statistics decryption).
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

from argparse import ArgumentParser
import matplotlib.pyplot as plt
from string import ascii_letters
from typing import Dict
from json import dumps
from sys import exit

__license__ = "GPL-3.0 License"
__copyright__ = """
FileAnalysis  Copyright (C) 2021  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
copyright = __copyright__
license = __license__

__version__ = "0.0.2"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = (
    "This file analyze emergence of characters in file (to decrypt with statistics)."
)
__url__ = "https://github.com/mauricelambert/FileAnalysis/"

__all__ = ["FileAnalysis", "FRENCH_FREQUENCE", "ENGLISH_FREQUENCE"]

FRENCH_FREQUENCE = {
    "E": 12.10,
    "A": 7.11,
    "I": 6.59,
    "S": 6.51,
    "N": 6.39,
    "R": 6.07,
    "T": 5.92,
    "O": 5.02,
    "L": 4.96,
    "U": 4.49,
    "D": 3.67,
    "C": 3.18,
    "M": 2.62,
    "P": 2.49,
    "G": 1.23,
    "B": 1.14,
    "V": 1.11,
    "H": 1.11,
    "F": 1.11,
    "Q": 0.65,
    "Y": 0.46,
    "X": 0.38,
    "J": 0.34,
    "K": 0.29,
    "W": 0.17,
    "Z": 0.15,
}

ENGLISH_FREQUENCE = {
    "E": 13,
    "T": 9.1,
    "A": 8.2,
    "O": 7.5,
    "I": 7,
    "N": 6.7,
    "S": 6.3,
    "H": 6.1,
    "R": 6,
    "D": 4.3,
    "L": 4,
    "U": 2.8,
    "C": 2.8,
    "W": 2.4,
    "M": 2.4,
    "F": 2.2,
    "G": 2,
    "Y": 2,
    "P": 1.9,
    "B": 1.5,
    "V": 0.98,
    "K": 0.77,
    "J": 0.15,
    "X": 0.15,
    "Q": 0.095,
    "Z": 0.074,
}


class FileAnalysis:

    """ This class analyze emergence of characters. """

    def __init__(self, filename: str, alphabet_only: bool = False):
        self.filename = filename
        self.alphabet_only = alphabet_only
        self.encoded_letters = ascii_letters.encode()
        self.compteur = 0
        self.chars = {}

    def analysis_filecontent(self) -> Dict[str, int]:

        """ This function analyze file content. """

        with open(self.filename, "rb") as file:
            char = " "
            while char:
                char = file.read(1)
                if char:
                    self.analysis_char(char)

        return self.chars

    def analysis_char(self, char: bytes) -> None:

        """ This function analyse a character. """

        if self.alphabet_only and char in self.encoded_letters:
            self.compteur += 1
            char = char.decode().upper()
            self.chars.setdefault(char, 0)
            self.chars[char] += 1
        elif not self.alphabet_only:
            self.compteur += 1
            char = chr(char[0])
            self.chars.setdefault(char, 0)
            self.chars[char] += 1

    def get_pourcent(self) -> Dict[str, float]:

        """ This function return pourcent from chars. """

        for char, emergence in self.chars.items():
            self.chars[char] = emergence / self.compteur * 100

        return self.chars

    def sort_and_show(self, sort: bool = False, json: bool = False) -> None:

        """This function sort characters by emergence
        if sort argument is True and print emergences as JSON
        if json argument is True else show chart."""

        if sort:
            self.chars = {
                k: self.chars[k]
                for k in sorted(self.chars, key=lambda x: self.chars[x])
            }

        if json:
            print(dumps(self.chars, indent=4))
        else:
            self.build_chart()

    def build_chart(self) -> None:

        """ This function use pyplot to build the chart from chars. """

        positions = range(len(self.chars))
        plt.bar(positions, self.chars.values())
        plt.xticks(positions, self.chars.keys())
        plt.title(f"File analysis: {self.filename}")
        plt.show()


def parse() -> ArgumentParser:

    """ This function parse arguments. """

    args = ArgumentParser(description="This programme analyze emergence of characters.")
    args.add_argument("--filename", "-f", help="Filename to analyze")
    args.add_argument(
        "--sorted",
        "-s",
        help="Sort character by emergence.",
        default=False,
        action="store_true",
    )
    args.add_argument(
        "--french-emergence",
        "-F",
        help="Show french emergence.",
        default=False,
        action="store_true",
    )
    args.add_argument(
        "--english-emergence",
        "-E",
        help="Show english emergence.",
        default=False,
        action="store_true",
    )
    args.add_argument(
        "--json",
        "-j",
        help="Print JSON data in console (no chart).",
        default=False,
        action="store_true",
    )
    args.add_argument(
        "--alphabet-only",
        "-a",
        help="Show chart with alphabet only.",
        default=False,
        action="store_true",
    )
    args.add_argument(
        "--number",
        "-n",
        help="Show chart with emergence character number (default is pourcent).",
        default=False,
        action="store_true",
    )

    return args


def main() -> None:
    args = parse().parse_args()
    if args.french_emergence:
        analysis = FileAnalysis("French emergence.")
        analysis.chars = FRENCH_FREQUENCE
        analysis.sort_and_show(args.sorted, args.json)
    elif args.english_emergence:
        analysis = FileAnalysis("English emergence.")
        analysis.chars = ENGLISH_FREQUENCE
        analysis.sort_and_show(args.sorted, args.json)
    elif args.filename:
        analysis = FileAnalysis(args.filename, alphabet_only=args.alphabet_only)
        analysis.analysis_filecontent()
        if not args.number:
            analysis.get_pourcent()
        analysis.sort_and_show(args.sorted, args.json)
    else:
        print(
            "OPTIONS REQUIRED: --filename/-f OR --french-emergence/-F OR --help/-h OR --english-emergence/-E"
        )
        exit(1)


if __name__ == "__main__":
    main()

print(copyright)
