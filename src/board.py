import curses


class Board():
    def __init__(self, board_size: int = 9) -> None:
        self.board_size = board_size
        self.value_dict = {_: ' ' for _ in range(0, board_size)}

    def is_valid_cell(self, index_cell: int) -> bool:
        return self.value_dict[index_cell] == ' '

    def is_full(self) -> bool:
        for i in range(self.board_size):

            if ' ' == self.value_dict[i]:
                return False

        return True

    def is_win(self, symbol: str) -> bool:
        # TODO: Оптимизировать позже.
        sqrt_board_size = int(self.board_size ** 0.5)

        # По горизонтали
        for i in range(0, self.board_size, sqrt_board_size):
            if self.value_dict[i] == symbol and \
                self.value_dict[i + 1] == symbol and \
                    self.value_dict[i + 2] == symbol:
                return True

        # По вертикали
        for i in range(sqrt_board_size):
            if self.value_dict[i] == symbol and \
                self.value_dict[i + sqrt_board_size] == symbol and \
                    self.value_dict[i + sqrt_board_size * 2] == symbol:
                return True

        # По диагонали \
        for i in range(self.board_size):
            try:
                if self.value_dict[i] == symbol and \
                    self.value_dict[i + sqrt_board_size + 1] == symbol and \
                        self.value_dict[i + sqrt_board_size * 2 + 2] == symbol:
                    return True
            except KeyError:
                continue

        # По диагонали /
        for i in range(2, self.board_size):
            try:
                if self.value_dict[i] == symbol and \
                    self.value_dict[i + sqrt_board_size - 1] == symbol and \
                        self.value_dict[i + sqrt_board_size * 2 - 2] == symbol:
                    return True
            except KeyError:
                continue

        return False

    def update_value_dict(self, index_cell: int, symbol: str) -> None:
        self.value_dict[index_cell] = symbol

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
