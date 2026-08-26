import curses

from src.core.board import Board

from .base import UI


class CursesUI(UI):
    def __init__(self, stdscr: curses.window) -> None:
        self.stdscr = stdscr
        self.stdscr.keypad(True)

        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def show_board(self, board: Board, cursor_pos: int) -> None:
        self.stdscr.clear()

        sqrt_size = int(board.board_size**0.5)
        y, x = 0, 0
        index = 0

        for _ in range(sqrt_size):
            self.stdscr.addstr(y, x, " -" + "----" * sqrt_size)
            y += 1

            for _ in range(index, index + sqrt_size):
                if cursor_pos == index:
                    self.stdscr.addstr(y, x, " | ")
                    self.stdscr.addstr(
                        y, x + 3, f"{board.value_list[index]}", curses.color_pair(1)
                    )
                else:
                    self.stdscr.addstr(y, x, f" | {board.value_list[index]}")

                index += 1
                x += 4

            self.stdscr.addstr(y, x, " | ")

            y += 1
            x = 0

        self.stdscr.addstr(y, x, " -" + "----" * sqrt_size)
        self.stdscr.refresh()

    def show_menu(self, options: list[str], title: str, cursor_pos: int) -> None:
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, title, curses.A_BOLD)

        y = 1

        for option in options:
            if y == cursor_pos:
                self.stdscr.addstr(y, 0, " > " + option, curses.color_pair(1))
            else:
                self.stdscr.addstr(y, 0, " - " + option)

            y += 1

        self.stdscr.refresh()

    def show_message(self, text: str) -> None:
        self.stdscr.clear()
        self.stdscr.addstr(10, 0, text)
        self.stdscr.refresh()
        self.stdscr.getch()

    def get_key(self) -> str:
        key = self.stdscr.getch()

        if key in (curses.KEY_UP, ord("w")):
            return "up"
        elif key in (curses.KEY_DOWN, ord("s")):
            return "down"
        elif key in (curses.KEY_LEFT, ord("a")):
            return "left"
        elif key in (curses.KEY_RIGHT, ord("d")):
            return "right"
        elif key in (ord("z"), ord("\n")):
            return "confirm"
        elif key == ord("x"):
            return "x"
        elif key == ord("q"):
            return "q"
        elif key == 27:
            return "escape"

        return ""
