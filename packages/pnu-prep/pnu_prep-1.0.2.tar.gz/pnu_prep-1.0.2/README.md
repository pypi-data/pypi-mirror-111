# Installation
pip install [pnu-prep](https://pypi.org/project/pnu-prep/)

# PREP(1)

## NAME
prep - prepare text for statistical processing

## SYNOPSIS
**prep**
\[-a|--ascii\]
\[-d|--number\]
\[-h|--hyphen\]
\[-i|--ignore FILE\]
\[-o|--only FILE\]
\[-p|--ponctuate\]
\[--debug\]
\[--help|-?\]
\[--version\]
\[--\]
\[file\]
\[...\]

## DESCRIPTION
**prep** reads each *file* in sequence and writes it on the standard output,
one lowercase `word' per line.
A word is a string of alphabetic characters and embedded apostrophes, delimited by space or punctuation.
Hyphenated words are broken apart;
hyphens at the end of lines are removed and the hyphenated parts are joined.
Strings of digits are discarded.

When no files are given as arguments, standard input is read (until a Control-D (Unix) or Control-Z (Windows) character is sent).

The following option letters may appear in any order:

### OPTIONS
Options | Use
------- | ---
-a\|--ascii|Try to convert Unicode letters to ASCII.
-d\|--number|Print the word number (in the input stream) with each word.
-h\|--hyphen|Don't break words on hyphens.
-i\|--ignore|Take the next *file* as an `ignore' file. These words will not appear in the output. (They will be counted, for purposes of the **-d** numbering.)
-o\|--only|Take the next *file* as an `only' file. Only these words will appear in the output. (All other words will also be counted for the **-d** numbering.)
-p\|--ponctuate|Include punctuation marks (single nonalphanumeric characters from the "!(),.:;?" set) as separate output lines. The punctuation marks are not counted for the **-d** numbering.
--debug|Enable debug mode
--help\|-?|Print usage and a short help message and exit
--version|Print version and exit
--|Options processing terminator

## FILES
Ignore and only files contain words, one per line.

The file [/usr/local/etc/eign](https://minnie.tuhs.org/cgi-bin/utree.pl?file=V7/usr/lib/eign) was originally provided in **/usr/lib** as an example or default ignore file.

## EXIT STATUS
The **prep** utility exits 0 on success, and >0 if an error occurs.

## SEE ALSO
[deroff(1)](http://man.cat-v.org/unix_7th/1/deroff)

## STANDARDS
The **prep** utility is a deprecated [UNIX 7th edition](https://minnie.tuhs.org/cgi-bin/utree.pl?file=V7) command (it also appeared in Unix V7M, Ultrix 3.1, 2.9BSD and 2.11BSD).

Our implementation tries to follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for [Python](https://www.python.org/) code.

## PORTABILITY
Tested OK under Windows.

## HISTORY
This utility was made for the [PNU project](https://github.com/HubTou/PNU), out of historical curiosity and for fun, though it doesn't seem very useful...

Some features were added compared to the original command:
* [Unicode](https://en.wikipedia.org/wiki/Unicode) letters are now supported by default (the original command predated Unicode by 12 years).
* It is now possible to use the **-i** and **-o** options at the same time.
* The **-h** option was added to avoid breaking word on hyphens, which makes sense in French.
* The **-a** option was added to try to convert Unicode accented letters to their ASCII equivalent.

Several bugs from the original **prep** command were corrected:
* A display bug on hyphenated words inside a line when used with the combined **-d** and **-p** options.
* A bug with lines starting by an apostrophe.
* A bug with the character following an apostrophe.

## LICENSE
This utility is available under the [3-clause BSD license](https://opensource.org/licenses/BSD-3-Clause).

## AUTHORS
[Hubert Tournier](https://github.com/HubTou)

