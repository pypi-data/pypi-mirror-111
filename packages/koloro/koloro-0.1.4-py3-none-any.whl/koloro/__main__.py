from shutil import get_terminal_size

import koloro

welcome = (
  f'{koloro.red("K")}'
  f'{koloro.green("o")}'
  f'{koloro.yellow("l")}'
  f'{koloro.blue("o")}'
  f'{koloro.magenta("r")}'
  f'{koloro.cyan("o")}'
  f' {koloro.dim("-")} '
  f'{koloro.brightCyan("colorful terminal text in Python.")}'
)

cols = get_terminal_size().columns // 10

print('\n' + welcome.center(cols))

print('\nColors:')

for c in (
  'black',
  'red',
  'green',
  'yellow',
  'blue',
  'magenta',
  'cyan',
  'white',
):
  print(getattr(koloro, c)(c.center(cols)), end='  ')

print('\n\nBright colors:')

for c in (
  'grey',
  'brightRed',
  'brightGreen',
  'brightYellow',
  'brightBlue',
  'brightMagenta',
  'brightCyan',
  'brightWhite',
):
  print(getattr(koloro, c)(c.center(cols)), end='  ')

print('\n\nBackground colors:')

for bgC, c in zip(
  (
    'bgBlack',
    'bgRed',
    'bgGreen',
    'bgYellow',
    'bgBlue',
    'bgMagenta',
    'bgCyan',
    'bgWhite',
  ),
  (
    koloro.white,
    koloro.black,
    koloro.black,
    koloro.black,
    koloro.black,
    koloro.black,
    koloro.black,
    koloro.black,
  ),
):
  txt = c(bgC.center(cols))  # type: ignore[operator]
  print(getattr(koloro, bgC)(txt), end='  ')

print('\n\nBright Background colors:')

for bgC, c in zip(
  (
    'bgGrey',
    'bgBrightRed',
    'bgBrightGreen',
    'bgBrightYellow',
    'bgBrightBlue',
    'bgBrightMagenta',
    'bgBrightCyan',
    'bgBrightWhite',
  ),
  (
    koloro.white,
    koloro.black,
    koloro.black,
    koloro.black,
    koloro.black,
    koloro.black,
    koloro.black,
    koloro.black,
  ),
):
  txt = c(bgC.center(cols))  # type: ignore[operator]
  print(getattr(koloro, bgC)(txt), end='  ')

print('\n\nModifiers:')

for m in (
  'reset',
  'bold',
  'dim',
  'italic',
  'underline',
  'inverse',
  'hidden',
  'strikethrough',
):
  print(getattr(koloro, m)(m.center(cols)), end='  ')


print('\n\nStrip ANSI codes:')

for c in (
  'black',
  'red',
  'green',
  'yellow',
  'blue',
  'magenta',
  'cyan',
  'white',
):
  print(koloro.strip_ansi(getattr(koloro, c)(c.center(cols))), end='  ')

print('\n\nANSI 256 colors:')

ansi256 = ''
for i in range(256):
  if (i + 1) % 8 == 0:
    ansi256 += '\n'
  ansi256 += f' {koloro.ansi256(i)("koloro")} '

print(ansi256)

print('\n\nANSI 256 background colors:')

ansi256Bg = ''
for i in range(256):
  if (i + 1) % 8 == 0:
    ansi256Bg += '\n\n'
  ansi256Bg += f' {koloro.ansi256Bg(i)(" koloro ")} '

print(ansi256Bg)
