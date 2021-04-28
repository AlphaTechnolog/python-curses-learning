import curses
import argparse
import asyncio
import os
import sys
from typing import Callable


class Diamond:
    def __init__(self: Callable, stdscr: Callable, diamond_delay: float) -> Callable:
        self.stdscr = stdscr
        self.diamond_delay = diamond_delay

    async def render(self: Callable):
        self.height, self.width = self.stdscr.getmaxyx()

        y = 0
        x = int(self.width / 2)

        while True:
            await asyncio.sleep(self.diamond_delay)
            if not y == 0:
                self.stdscr.addstr(y, x, '*', curses.color_pair(1))
            self.stdscr.move(self.height - 1, self.width - 1)
            self.stdscr.refresh()
            
            if y == int(self.height / 2):
                break
            
            y += 1
            x -= 1
            
        while True:
            await asyncio.sleep(self.diamond_delay)
            self.stdscr.addstr(y, x, '*', curses.color_pair(1))
            self.stdscr.move(self.height - 1, self.width - 1)
            self.stdscr.refresh()

            if y == int(self.height - 1):
                break

            y += 1
            x += 1
            
        while True:
            await asyncio.sleep(self.diamond_delay)
            self.stdscr.addstr(y, x, '*', curses.color_pair(1))
            self.stdscr.move(self.height - 1, self.width - 1)
            self.stdscr.refresh()

            if y == int(self.height / 2):
                break
            
            y -= 1
            x += 1
            
        while True:
            await asyncio.sleep(self.diamond_delay)
            self.stdscr.addstr(y, x, '*', curses.color_pair(1))
            self.stdscr.move(self.height - 1, self.width - 1)
            self.stdscr.refresh()

            if y == 1:
                break
            
            y -= 1
            x -= 1

        self.stdscr.move(self.height - 1, self.width - 1)


class Author:
    def __init__(self: Callable, stdscr: Callable, author_text_delay: float) -> Callable:
        self.stdscr = stdscr
        self.delay = author_text_delay

    async def render(self: Callable):
        self.height, self.width = self.stdscr.getmaxyx()
        word = 'Written by: Gabriel Guerra'
        omit_word = 'Press any key to exit...'
        i = 0

        for char in word:
            self.stdscr.addstr(
                self.height - 2,
                self.width - 1 - (len(word) - i),
                char,
                curses.color_pair(2)
            )

            self.stdscr.refresh()
            await asyncio.sleep(self.delay)
            i += 1
            
        i = 0

        for char in omit_word:
            self.stdscr.addstr(
                self.height - 1,
                self.width - 3 - (len(omit_word) - i),
                char,
                curses.color_pair(3)
            )

            self.stdscr.refresh()
            await asyncio.sleep(self.delay)
            i += 1


async def main(stdscr):
    parser = argparse.ArgumentParser(
        prog='diamond-generator',
        description='A diamond generator based in the python curses library'
    )
    
    parser.add_argument(
        '-D', '--diamond-delay',
        type=float, help='Diamond animation delay',
        default=0.05, required=False
    )
    
    parser.add_argument(
        '--no-author-text',
        action='store_true',
        help='No show the author text.'
    )
    
    parser.add_argument(
        '-Ad', '--author-text-delay',
        type=float, help='Delay of author text animation',
        default=0.12, required=False
    )
    
    args = parser.parse_args()
    
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    diamond = Diamond(stdscr=stdscr, diamond_delay=args.diamond_delay)
    author = Author(stdscr=stdscr, author_text_delay=args.author_text_delay)
    await diamond.render()
    
    if not args.no_author_text:
        await author.render()
    
    stdscr.getkey()


async def realmain():
    await curses.wrapper(main)


if __name__ == '__main__':
    asyncio.run(realmain())
