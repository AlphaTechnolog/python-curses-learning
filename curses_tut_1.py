import curses
from typing import Any
from os import system
from os import name as osname


def clear():
    cmd = 'clear' if osname != 'nt' else 'cls'
    system(cmd)


def bye():
    clear()
    print('Bye bye...')
    exit(0)


def main(stdscr: Any):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.addstr(0, 0, 'Press q to exit!')
    stdscr.refresh()

    key = ''

    while key != 'q':
        key = stdscr.getkey()
        stdscr.addstr(1, 0, 'Key pressed: {}'.format(key))
        stdscr.refresh()


if __name__ == '__main__':
    curses.wrapper(main)
    bye()
