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
        self.stdscr.border(0)

        height, width = self.stdscr.getmaxyx()
        sqrt_size = int(board.board_size**0.5)

        board_height = sqrt_size * 2 + 1
        board_width = 2 + 4 * sqrt_size

        start_y = (height - board_height) // 2
        start_x = (width - board_width) // 2 - 1

        y, x = start_y, start_x
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
            x = start_x

        self.stdscr.addstr(y, x, " -" + "----" * sqrt_size)
        self.stdscr.refresh()

    def show_menu(self, options: list[str], title: str, cursor_pos: int) -> None:
        self.stdscr.clear()
        self.stdscr.border(0)

        height, width = self.stdscr.getmaxyx()
        menu_height = 2 + len(options)

        start_y = (height - menu_height) // 2
        start_x = (width - len(title)) // 2

        self.stdscr.addstr(start_y, start_x, title, curses.A_BOLD)

        y = start_y + 2
        highlighted_line = y + cursor_pos - 1

        for opt in options:
            if y == highlighted_line:
                self.stdscr.addstr(y, start_x, " > " + opt, curses.color_pair(1))
            else:
                self.stdscr.addstr(y, start_x, " - " + opt)

            y += 1

        self.stdscr.refresh()

    def show_message(self, text: str) -> None:
        self.stdscr.clear()
        self.stdscr.border(0)
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
