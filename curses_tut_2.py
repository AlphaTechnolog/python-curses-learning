import curses
import subprocess
from os.path import expanduser
from random import randint
from typing import Callable, Any
from pathlib import Path


def exe(cmd: str) -> str or None:
    executer = subprocess.run(
        [cmd],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    return executer.stdout.decode('utf-8')


def user() -> Path:
    return Path(expanduser('~'))


class Logger:
    def __init__(self: Callable, father: Callable, stdscr: Any, win_x: int, win_y: int) -> Callable:
        self.father = father
        self.stdscr = stdscr
        self.win_x = win_x
        self.win_y = win_y

    def simple_statusbar(self: Callable, stbrstr: str):
        self.stdscr.addstr(0, 0, stbrstr, self.father.paint(1))
        self.stdscr.addstr(0, len(stbrstr), ' ' * ((self.win_x - 1) - len(stbrstr)), self.father.paint(1))

    def simple_continue_msg(self: Callable):
        text = 'Press any key to continue...'
        self.stdscr.addstr(self.win_y - 1, self.win_x - 1 - len(text), text, self.father.paint(6))

    def error(self: Callable, msg: str):
        self.stdscr.clear()
        self.simple_statusbar('-- ERROR --')
        self.stdscr.addstr(1, 0, msg, self.father.paint(4))
        self.simple_continue_msg()
        self.stdscr.refresh()
        self.father.cursor.move_to_end()
        self.stdscr.getkey()
        self.stdscr.clear()
        self.father.run()

    def display(self: Callable, *argv):
        i = 1

        self.stdscr.clear()

        for color, msg in argv:
            self.stdscr.addstr(i, 0, msg, color)
            i += 1

        self.stdscr.refresh()
        self.simple_statusbar('-- MESSAGE --')
        self.simple_continue_msg()
        self.father.cursor.move_to_end()
        self.stdscr.getkey()
        self.stdscr.clear()
        self.father.run()


class OrderLineActions:
    def __init__(self: Callable, father: Callable, stdscr: Any, win_x: int, win_y: int) -> Callable:
        self.father = father

        self.commands = {
            'q': lambda: exit(0),
            'quit': lambda: exit(0),
            'help': self._command__help,
            'h': self._command__help,
            'w': self._command__write,
            'write': self._command__write
        }

        self.logger = Logger(
            father=father,
            stdscr=stdscr,
            win_x=win_x,
            win_y=win_y
        )

        self.stdscr = stdscr
        self.win_x = win_x
        self.win_y = win_y

    def _command__write(self: Callable):
        dir_path = user() / Path('.curses_test_screenshots')

        if not dir_path.is_dir():
            dir_path.mkdir()

        name = f'{randint(1, 10000001)}.png'
        exe(f'scrot "./{name}"')
        exe(f'mv "./{name}" {str(dir_path)}')

        self.logger.display(
            (self.father.paint(2), 'Created screenshot!'),
            (self.father.paint(5), '  At: ~/.curses_test_screenshots')
        )

    def _command__help(self: Callable):
        self.logger.display(
            (self.father.paint(2), 'Available commands:',),
            (self.father.paint(2), ''),
            (self.father.paint(5), '  :q | :quit => Exit'),
            (self.father.paint(5), '  :h | :help => Show this message'),
            (self.father.paint(5), ''),
            (self.father.paint(2), 'Shortcuts:',),
            (self.father.paint(5), '',),
            (self.father.paint(5), '  q => Exit'),
            (self.father.paint(5), '  h => Show this message'),
        )

    def _invoke(self: Callable, key: str):
        if not key in self.commands:
            return self.logger.error(f'Invalid command: {key}')

        self.commands[key]()

    def run(self: Callable, key: str):
        self.stdscr.clear()
        self._invoke(key)
        self.stdscr.refresh()


class OrderLine:
    excepting_keys = [
        'KEY_BACKSPACE',
        '\n'
    ]

    def __init__(self: Callable, stdscr: Any, win_y: int, win_x: int, self_ins: Callable) -> Callable:
        self.order_line_actions = OrderLineActions(
            father=self_ins,
            stdscr=stdscr,
            win_x=win_x,
            win_y=win_y
        )

        self.stdscr = stdscr
        self.win_y = win_y
        self.win_x = win_x
        self.father = self_ins
        self.key = None
        self.word = ''

    def update_word(self: Callable) -> bool:
        if not self.key in self.excepting_keys:
            self.word += self.key
            return True

        return False

    def minus_word(self: Callable) -> bool:
        if len(self.word) > 0:
            self.word = self.word[:len(self.word) - 1]
            return True

        return False

    def update_input_text(self: Callable):
        self.stdscr.addstr(self.win_y - 1, 0, ' ' * (self.win_y - 1))
        self.stdscr.addstr(self.win_y - 1, 0, ':')
        self.stdscr.addstr(self.win_y - 1, 1, get_text(self.word, win_width=self.win_x))

    def start_input(self: Callable):
        while True:
            self.key = self.stdscr.getkey()

            if (self.key == 'KEY_BACKSPACE' and
                    len(self.word) == 0):
                self.stdscr.addstr(self.win_y - 1, 0, ' ' * (self.win_x - 1))
                break
            elif self.key == 'KEY_BACKSPACE':
                self.minus_word()
            else:
                self.update_word()

            self.update_input_text()
            self.stdscr.refresh()

            if self.key == '\n':
                self.order_line_actions.run(self.word)
                break

    def run(self: Callable):
        self.stdscr.addstr(self.win_y - 1, 0, ':')
        self.stdscr.refresh()
        self.start_input()
        self.father.run(first_refreshing=False)


class Cursor:
    def __init__(self: Callable, stdscr: Any, win_y: int, win_x: int, self_ins: Callable) -> Callable:
        self.stdscr = stdscr
        self.win_y = win_y
        self.win_x = win_x
        self.x = self.getx(0)
        self.y = self.gety(0)
        self.father = self_ins

    def gety(self: Callable, pos: int) -> int:
        res: int = max(0, pos)
        return min(self.win_y - 1, res)

    def getx(self: Callable, pos: int) -> int:
        res: int = max(0, pos)
        return min(self.win_x - 1, res)

    def update_cursor_pos(self: Callable):
        self.stdscr.move(self.y, self.x)

    def move_to_start(self: Callable):
        self.x = self.getx(0)
        self.y = self.gety(0)
        self.update_cursor_pos()

    def move_to_end(self: Callable):
        self.x = self.getx(self.win_x - 1)
        self.y = self.gety(self.win_y - 1)
        self.update_cursor_pos()

    def check_movement(self: Callable, key: int) -> bool:
        changed: bool = False

        if key == curses.KEY_DOWN:
            self.y = self.gety(self.y + 1)
            changed = True
        elif key == curses.KEY_UP:
            self.y = self.gety(self.y - 1)
            changed = True
        elif key == curses.KEY_RIGHT:
            self.x = self.getx(self.x + 1)
            changed = True
        elif key == curses.KEY_LEFT:
            self.x = self.getx(self.x - 1)
            changed = True
        elif key == ord('Ũ'):
            self.x = self.getx(self.win_x - 1)
            changed = True
        elif key == ord('Ć'):
            self.x = self.getx(0)
            changed = True

        if changed:
            self.update_cursor_pos()

        return changed


def get_text(text: str, win_width: int) -> str:
    return text[:win_width - 1]


AUTHOR='Gabriel Guerra'


class StatusBar:
    def __init__(self: Callable, stdscr: Any, pair: Any, secondary_pair: Any, width: int, height: int, self_ins: Callable) -> Callable:
        self.pair = pair
        self.secondary_pair = secondary_pair
        self.width = width
        self.height = height
        self.stdscr = stdscr
        self.father = self_ins

    def get_statusbarstr(self: Callable) -> str:
        return get_text(
            f'Press q to exit | Window data: x = {self.width}, y = {self.height}',
            win_width=self.width
        )

    def get_authorstr(self: Callable) -> str:
        return get_text(
            f'Written by: {AUTHOR}',
            win_width=self.width
        )

    def get_statusbar_spaces(self: Callable) -> str:
        return " " * (self.width - len(self.get_statusbarstr()) - 1 - len(self.get_authorstr()))

    def render(self: Callable):
        self.stdscr.attron(self.pair)
        self.stdscr.addstr(self.height - 2, 0, self.get_statusbarstr())
        self.stdscr.addstr(self.height - 2, len(self.get_statusbarstr()), self.get_statusbar_spaces())
        self.stdscr.addstr(self.height - 2, len(self.get_statusbar_spaces()) + len(self.get_statusbarstr()), self.get_authorstr())
        self.stdscr.attroff(self.pair)


class App:
    def __init__(self: Callable) -> Callable:
        self.curses = curses
        self.curses.wrapper(self.init_stdscr)

    def get_scr_meta(self: Callable):
        self.y, self.x = self.stdscr.getmaxyx()

    def set_scr_colors(self: Callable):
        self.curses.start_color()

        self.curses.init_pair(
            1,
            self.curses.COLOR_BLACK,
            self.curses.COLOR_WHITE
        )

        self.curses.init_pair(
            2,
            self.curses.COLOR_CYAN,
            self.curses.COLOR_BLACK
        )

        self.curses.init_pair(
            3,
            self.curses.COLOR_RED,
            self.curses.COLOR_BLACK
        )

        self.curses.init_pair(
            4,
            self.curses.COLOR_RED,
            self.curses.COLOR_BLACK
        )

        self.curses.init_pair(
            5,
            self.curses.COLOR_WHITE,
            self.curses.COLOR_BLACK
        )

        self.curses.init_pair(
            6,
            self.curses.COLOR_MAGENTA,
            self.curses.COLOR_BLACK
        )

    def init_stdscr(self: Callable, stdscr: Any):
        self.stdscr = self.curses.initscr()
        self.initial_screen_parameters()
        self.get_scr_meta()
        self.set_scr_colors()
        self.run()

    def initial_screen_parameters(self: Callable):
        self.stdscr.clear()
        self.curses.noecho()
        self.curses.cbreak()
        self.stdscr.keypad(True)

    def getkey(self: Callable):
        self.key = self.stdscr.getch()

    def init_statusbar(self: Callable):
        self.statusbar = StatusBar(
            pair=self.paint(1),
            secondary_pair=self.paint(4),
            self_ins=self,
            stdscr=self.stdscr,
            width=self.x,
            height=self.y
        )

        self.statusbar.render()

    def paint(self: Callable, pallet: int) -> Any:
        return self.curses.color_pair(pallet)

    def init_app_works(self: Callable):
        while self.key != ord('q') and self.key != ord(':'):
            self.getkey()

            if self.key == ord(';'):
                break

            if self.key == ord('h'):
                self.order_line_actions.run('help')

            if not self.cursor.check_movement(key=self.key) and not self.key == ord(':'):
                self.stdscr.addstr(self.y - 2, 0, '')
                self.stdscr.addstr(0, 0, f'Pressed key: {chr(self.key)}', self.paint(2))
                self.cursor.move_to_start()
                self.stdscr.refresh()

    def run(self: Callable, first_refreshing=True):
        self.cursor = Cursor(
            stdscr=self.stdscr,
            win_y=self.y,
            win_x=self.x,
            self_ins=self
        )

        self.order_line_actions = OrderLineActions(
            father=self,
            stdscr=self.stdscr,
            win_x=self.x,
            win_y=self.y
        )

        if first_refreshing:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, ' ' * (self.x - 1))
            self.stdscr.addstr(0, 0, 'No key pressed', self.paint(3))
            self.init_statusbar()
            self.stdscr.refresh()

        self.key = ''
        self.cursor.move_to_start()
        self.init_app_works()

        if self.key == ord(':') or self.key == ord(';'):
            self.order_line = OrderLine(
                stdscr=self.stdscr,
                win_y=self.y,
                win_x=self.x,
                self_ins=self
            )

            self.order_line.run()

def main():
    App()


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt):
        pass
