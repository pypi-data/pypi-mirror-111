"""Koloro - colorful terminal text in Python."""

import os
import re
import sys
from typing import Union

__version__ = '0.1.4'


def __is_enabled():
  NO_COLOR = os.getenv('NO_COLOR')
  TERM = os.getenv('TERM')
  FORCE_COLOR = os.getenv('FORCE_COLOR')

  if FORCE_COLOR:
    return True
  else:
    return TERM != 'dumb' and NO_COLOR is None and sys.stdout.isatty()


enabled = __is_enabled()


def koloro(x: Union[int, str], y: int):
  start = f'\x1b[{x}m'
  end = f'\x1b[{y}m'

  def _transform(txt: str) -> str:
    if enabled:
      # to support nested colors
      return start + txt.replace(end, start) + end
    return txt

  return _transform


# modifiers
reset = koloro(0, 0)
bold = koloro(1, 22)
dim = koloro(2, 22)
italic = koloro(3, 23)
underline = koloro(4, 24)
inverse = koloro(7, 27)
hidden = koloro(8, 28)
strikethrough = koloro(9, 29)

# colors
black = koloro(30, 39)
red = koloro(31, 39)
green = koloro(32, 39)
yellow = koloro(33, 39)
blue = koloro(34, 39)
magenta = koloro(35, 39)
cyan = koloro(36, 39)
white = koloro(37, 39)

# background colors
bgBlack = koloro(40, 49)
bgRed = koloro(41, 49)
bgGreen = koloro(42, 49)
bgYellow = koloro(43, 49)
bgBlue = koloro(44, 49)
bgMagenta = koloro(45, 49)
bgCyan = koloro(46, 49)
bgWhite = koloro(47, 49)

# bright colors
grey = gray = koloro(90, 39)
brightRed = koloro(91, 39)
brightGreen = koloro(92, 39)
brightYellow = koloro(93, 39)
brightBlue = koloro(94, 39)
brightMagenta = koloro(95, 39)
brightCyan = koloro(96, 39)
brightWhite = koloro(97, 39)

# bright background colors
bgGrey = bgGray = koloro(100, 49)
bgBrightRed = koloro(101, 49)
bgBrightGreen = koloro(102, 49)
bgBrightYellow = koloro(103, 49)
bgBrightBlue = koloro(104, 49)
bgBrightMagenta = koloro(105, 49)
bgBrightCyan = koloro(106, 49)
bgBrightWhite = koloro(107, 49)


def ansi256(n: int):
  """Factory function for returning ANSI 256 color function with given n.

  Arguments:
    n: color code from ANSI 256

  Example:

  ```py
  >>> text = 'test'
  >>> print(ansi256(9)(text))  # red colored 'test'
  test

  ```
  """

  num: str = str(n)
  return koloro('38;5;' + num, 0)


def ansi256Bg(n: int):
  """Factory function for returning ANSI 256 color function for background
  with given n.

  Arguments:
    n: color code from ANSI 256

  Example:

  ```py
  >>> text = 'test'
  >>> print(ansi256Bg(9)(text))  # red background colored 'test'
  test

  ```
  """
  num: str = str(n)
  return koloro('48;5;' + num, 0)


def strip_ansi(string: str) -> str:
  """Strip ANSI code from given string.

  Arguments:
    string: ANSI colored string

  Example:

  ```py
  >>> text = '\x1b[32mtest\x1b[39m'
  >>> print(strip_ansi(text))
  test

  ```
  """
  return re.sub(r'\x1b\[[0-9;]+m', '', string)
