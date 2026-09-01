from abc import ABC, abstractmethod

from src.ui.base import UI

from .board import Board


class Player(ABC):
    def __init__(self, name: str, symbol: str, score: int = 0) -> None:
        self.name = name
        self.symbol = symbol
        self.score = score

    def __str__(self) -> str:
        return f"Имя: {self.name}, текущий счёт: {self.score}"

    @abstractmethod
    def make_move(self, board: Board, ui: UI) -> bool:
        pass


class HumanPlayer(Player):
    def __init__(self, name: str, symbol: str, score: int = 0) -> None:
        super().__init__(name, symbol, score)

    def make_move(self, board: Board, ui: UI) -> bool:
        cursor_pos = 0
        sqrt_size = int(board.board_size**0.5)

        while True:
            ui.show_board(board, cursor_pos)

            key = ui.get_key()

            if key == "q":
                return False
            elif key == "confirm":
                if board.is_valid_cell(cursor_pos):
                    board.update_value_list(cursor_pos, self.symbol)
                    return True
            else:
                cursor_pos = self._move_board_cursor(
                    key, cursor_pos, board.board_size, sqrt_size
                )

    def _move_board_cursor(
        self, key: str, cursor_pos: int, board_size: int, sqrt_size: int
    ) -> int:
        if key == "up":
            if cursor_pos // sqrt_size > 0:
                cursor_pos -= sqrt_size
        elif key == "down":
            if cursor_pos // sqrt_size < board_size // sqrt_size - 1:
                cursor_pos += sqrt_size
        elif key == "left":
            if cursor_pos % sqrt_size > 0:
                cursor_pos -= 1
        elif key == "right":
            if cursor_pos % sqrt_size < sqrt_size - 1:
                cursor_pos += 1

        return cursor_pos
