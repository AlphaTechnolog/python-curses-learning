import curses
import asyncio
from random import randint
from typing import Callable


async def realmain(stdscr: Callable, x_movement: int, y_movement: int):
    curses.noecho()
    curses.cbreak()

    height, width = stdscr.getmaxyx()
    height -= 1
    width -= 1

    y = 0 + y_movement
    x = int((width / 2)) + x_movement
    min_y = 0 + y_movement
    max_y = int(height) + y_movement
    min_x = int((width / 2) - (height / 2)) + x_movement
    max_x = int((width / 2) + (height / 2)) + x_movement

    mode_y = 'add'
    mode_x = 'substract'
    limit = 0
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    
    while limit != (height * 2):
        limit += 1
        
        if (x >= 1 and
                x <= width - 1 and
                y >= 1 and
                y <= height - 1):
            stdscr.addstr(y, x, '*', curses.color_pair(1))

        stdscr.refresh()
        await asyncio.sleep(randint(1, 26) / 2500)
    
        if mode_y == 'add':
            y += 1
        else:
            y -= 1
            
        if y == max_y:
            mode_y = 'substract'

        if y == min_y:
            mode_y = 'add'

        if mode_x == 'add':
            x += 1
        else:
            x -= 1

        if x == max_x:
            mode_x = 'substract'

        if x == min_x:
            mode_x = 'add'


async def main():
    try:
        i = 0
        
        while True:
            await curses.wrapper(lambda stdscr: realmain(
                curses.initscr(),
                randint(-50, 51),
                randint(-50, 51)
            ))
            
            i += 1
            
            if i == 20:
                i = 0
                stdscr = curses.initscr()
                stdscr.clear()
    except (KeyboardInterrupt):
        stdscr = curses.initscr()
        stdscr.getkey()
        curses.echo()
        curses.nocbreak()
        exit(0)


if __name__ == '__main__':
    asyncio.run(main())
