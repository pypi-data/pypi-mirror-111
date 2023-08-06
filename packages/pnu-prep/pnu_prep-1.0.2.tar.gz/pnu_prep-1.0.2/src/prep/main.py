#!/usr/bin/env python
""" prep - prepare text for statistical processing
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import getopt
import logging
import os
import string
import sys
import unicodedata

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: prep - prepare text for statistical processing v1.0.2 (July 3, 2021) by Hubert Tournier $"

# Default parameters. Can be overcome by environment variables, then command line options
parameters = {
    "Ascii": False,
    "Number": False,
    "Hyphen": False,
    "Ignore": "",
    "Only": "",
    "Ponctuate": False
}

PONCTUATION = "!(),.:;?"

################################################################################
def display_help():
    """Displays usage and help"""
    print("usage: prep [-a|--ascii] [-d|--number] [-h|--hyphen]", file=sys.stderr)
    print("       [-i|--ignore FILE] [-o|--only FILE] [-p|--ponctuate] [--debug]", file=sys.stderr)
    print("       [--help|-?] [--version] [--] filename [...]", file=sys.stderr)
    print("  ------------------  ------------------------------------------------", file=sys.stderr)
    print("  -a|--ascii          Try to convert Unicode letters to ASCII", file=sys.stderr)
    print("  -d|--number         Print the word number", file=sys.stderr)
    print("  -h|--hyphen         Don't break words on hyphens", file=sys.stderr)
    print("  -i|--ignore FILE    Take the next file as an ignore file", file=sys.stderr)
    print("  -o|--only FILE      Take the next file as an only file", file=sys.stderr)
    print("  -p|--ponctuate      Include punctuation marks", file=sys.stderr)
    print("  --debug             Enable debug mode", file=sys.stderr)
    print("  --help|-?           Print usage and this help message and exit", file=sys.stderr)
    print("  --version           Print version and exit", file=sys.stderr)
    print("  --                  Options processing terminator", file=sys.stderr)
    print(file=sys.stderr)


################################################################################
def process_command_line():
    """Process command line options"""
    # pylint: disable=C0103
    global parameters
    # pylint: enable=C0103

    # option letters followed by : expect an argument
    # same for option strings followed by =
    character_options = "adhi:o:p?"
    string_options = [
        "ascii",
        "debug",
        "help",
        "hyphen",
        "ignore",
        "number",
        "only",
        "ponctuate",
        "version",
    ]

    try:
        options, remaining_arguments = getopt.getopt(
            sys.argv[1:], character_options, string_options
        )
    except getopt.GetoptError as error:
        logging.critical("Syntax error: %s", error)
        display_help()
        sys.exit(1)

    for option, argument in options:

        if option in ("-a", "--ascii"):
            parameters["Ascii"] = True

        elif option in ("-d", "--number"):
            parameters["Number"] = True

        elif option in ("-h", "--hyphen"):
            parameters["Hyphen"] = True

        elif option in ("-i", "--ignore"):
            if os.path.isfile(argument):
                parameters["Ignore"] = argument
            else:
                logging.critical("-h|--ignore argument is not a file")
                sys.exit(1)

        elif option in ("-o", "--only"):
            if os.path.isfile(argument):
                parameters["Only"] = argument
            else:
                logging.critical("-o|--only argument is not a file")
                sys.exit(1)

        elif option in ("-p", "--ponctuate"):
            parameters["Ponctuate"] = True

        elif option == "--debug":
            logging.disable(logging.NOTSET)

        elif option in ("--help", "-?"):
            display_help()
            sys.exit(0)

        elif option == "--version":
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

    logging.debug("process_command_line(): parameters:")
    logging.debug(parameters)
    logging.debug("process_command_line(): remaining_arguments:")
    logging.debug(remaining_arguments)

    return remaining_arguments


################################################################################
def load_words_file(filename):
    """Load an ignore or only file as a list of words"""
    if not filename:
        return []

    with open(filename, "r") as file:
        return file.read()


################################################################################
def print_word(word, ignore_words, only_words, word_number):
    """Print a word in the different formats if needed"""
    if word not in ignore_words:
        if (not only_words) or word in only_words:
            if parameters["Number"]:
                print("{: 6d} {}".format(word_number, word))
            else:
                print(word)


################################################################################
def is_unicode_letter(character):
    """Return True if character is a Unicode letter"""
    if ord(character) > 127:
        return unicodedata.category(character)[0] == 'L'

    return False


################################################################################
def to_ascii(character):
    """Return Unicode letters to their ASCII equivalent and the rest unchanged"""
    if parameters["Ascii"] and ord(character) > 127:
        return unicodedata.normalize('NFKD', character).encode('ASCII', 'ignore').decode("utf-8")

    return character


################################################################################
def process_file(file, ignore_words, only_words, word_number):
    """Process a file and return the last word_number"""
    word = ""
    hyphen = False
    for line in file.readlines():
        for character in line.strip():
            if not word:
                if character in string.ascii_letters \
                or is_unicode_letter(character):
                    word = to_ascii(character.lower())
                elif parameters["Ponctuate"] and character in PONCTUATION:
                    print_word(character, [], [], 0)

            # hyphen inside a line:
            elif hyphen:
                print_word(word, ignore_words, only_words, word_number)
                word_number += 1
                if character in string.ascii_letters \
                or is_unicode_letter(character):
                    word = to_ascii(character.lower())
                else:
                    word = ""
                    if parameters["Ponctuate"] and character in PONCTUATION:
                        print_word(character, [], [], 0)
                hyphen = False

            else:
                if character in string.ascii_letters + "'" \
                or is_unicode_letter(character):
                    word += to_ascii(character.lower())
                elif character == "-":
                    if parameters["Hyphen"]:
                        word += "-"
                    else:
                        hyphen = True
                        # Let's see if next character is the end of line or not
                else:
                    if word[-1:] == "-":
                        word = word[:-1]
                    print_word(word, ignore_words, only_words, word_number)
                    word_number += 1
                    word = ""

                    if parameters["Ponctuate"] and character in PONCTUATION:
                        print_word(character, [], [], 0)

        # This is the end... of the line
        if word:
            if word[-1:] == "-":
                word = word[:-1]

            # hyphen at the end of line:
            elif hyphen:
                hyphen = False

            else:
                print_word(word, ignore_words, only_words, word_number)
                word_number += 1
                word = ""

    return word_number


################################################################################
def main():
    """The program's main entry point"""
    program_name = os.path.basename(sys.argv[0])
    console_log_format = program_name + ": %(levelname)s: %(message)s"
    logging.basicConfig(format=console_log_format, level=logging.DEBUG)
    logging.disable(logging.INFO)

    arguments = process_command_line()

    ignore_words = load_words_file(parameters["Ignore"])
    only_words = load_words_file(parameters["Only"])

    word_number = 1
    if len(arguments) :
        for filename in arguments:
            if not os.path.isfile(filename):
                continue

            with open(filename, "r") as file:
                word_number = process_file(file, ignore_words, only_words, word_number)
    else:
        # Filtering standard input:
        process_file(sys.stdin, ignore_words, only_words, word_number)

    sys.exit(0)


if __name__ == "__main__":
    main()
