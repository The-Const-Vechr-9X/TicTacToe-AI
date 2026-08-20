import curses


class Board():
    def __init__(self, board_size: int = 9) -> None:
        self.board_size = board_size
        self.value_dict = {_: ' ' for _ in range(0, board_size)}

    def draw(self, stdscr: curses.window, highlight_pos: int | None = None) -> None:
        sqrt_board_size = int(self.board_size ** 0.5)
        curses.curs_set(0)
        stdscr.clear()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        index = 0
        y, x = 0, 0

        for _ in range(sqrt_board_size):
            stdscr.addstr(y, x, " -" + "----" * sqrt_board_size)
            y += 1

            for _ in range(index, index + sqrt_board_size):

                if highlight_pos == index:
                    stdscr.addstr(y, x, " | ")
                    stdscr.addstr(y, x + 3, f"{self.value_dict[index]}", curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, f" | {self.value_dict[index]}")

                index += 1
                x += 4

            stdscr.addstr(y, x, " | ")

            y += 1
            x = 0

        stdscr.addstr(y, x, " -" + "----" * sqrt_board_size)
        stdscr.refresh()
