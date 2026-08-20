from abc import ABC, abstractmethod
from .board import Board
import curses


class Player(ABC):
    def __init__(self, name: str, symbol: str, score: int = 0) -> None:
        self.name = name
        self.symbol = symbol
        self.score = score

    def __str__(self) -> str:
        return f"Имя: {self.name}, текущий счёт: {self.score}"

    @abstractmethod
    def make_move(self, board: Board, stdscr: curses.window) -> None:
        pass

class HumanPlayer(Player):
    def __init__(self, name: str, symbol: str, score: int = 0) -> None:
        super().__init__(name, symbol, score)

    def make_move(self, board: Board, stdscr: curses.window):
        cursor = 0
        sqrt_board_size = int(board.board_size ** 0.5)
        stdscr.keypad(True)

        while True:
            board.draw(stdscr, cursor)

            key = stdscr.getch()

            if key == ord('q'):
                return None
            elif key in (ord('z'), ord('\n')):
                if board.is_valid_cell(cursor):
                    board.update_value_dict(cursor, self.symbol)
                    return None
            else:
                cursor = self._move_cursor(key, cursor, board.board_size, sqrt_board_size)

    def _move_cursor(self, key: int, cursor: int, board_size: int, sqrt_board_size: int) -> int:
        if key in (curses.KEY_UP, ord('w')):
            if cursor // sqrt_board_size > 0:
                cursor -= sqrt_board_size
        elif key in (curses.KEY_DOWN, ord('s')):
            if cursor // sqrt_board_size < board_size // sqrt_board_size - 1:
                cursor += sqrt_board_size
        elif key in (curses.KEY_LEFT, ord('a')):
            if cursor % sqrt_board_size > 0:
                cursor -= 1
        elif key in (curses.KEY_RIGHT, ord('d')):
            if cursor % sqrt_board_size < sqrt_board_size - 1:
                cursor += 1

        return cursor
