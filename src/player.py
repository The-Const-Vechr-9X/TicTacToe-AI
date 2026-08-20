from abc import ABC, abstractmethod
from board import Board
import curses


class Player(ABC):
    def __init__(self, name: str, symbol: str, score: int = 0) -> None:
        self.name = name
        self.symbol = symbol
        self.score = score

    def __str__(self) -> str:
        return f"Имя: {self.name}, текущий счёт: {self.score}"

    @abstractmethod
    def make_move(self, board: Board, stdscr: curses.window):
        pass

class HumanPlayer(Player):
    def __init__(self, name: str, symbol: str, score: int = 0) -> None:
        super().__init__(name, symbol, score)

    def make_move(self, board: Board, stdscr: curses.window):
        highlight_pos = 0
        sqrt_board_size = int(board.board_size ** 0.5)
        stdscr.keypad(True)

        while True:
            board.draw(stdscr, highlight_pos)

            key = stdscr.getch()

            if key == curses.KEY_UP:
                if highlight_pos // sqrt_board_size > 0:
                    highlight_pos -= sqrt_board_size
            elif key == curses.KEY_DOWN:
                if highlight_pos // sqrt_board_size < board.board_size // sqrt_board_size - 1:
                    highlight_pos += sqrt_board_size
            elif key == curses.KEY_LEFT:
                if highlight_pos % sqrt_board_size > 0:
                    highlight_pos -= 1
            elif key == curses.KEY_RIGHT:
                if highlight_pos % sqrt_board_size < sqrt_board_size - 1:
                    highlight_pos += 1

            elif key == ord('q'):
                return None
