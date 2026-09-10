from abc import ABC, abstractmethod
from random import randint

from src.ui.base import UI

from .board import Board
from .settings import Settings


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


class PlayerFactory:
    @staticmethod
    def create_players(settings: Settings) -> list[Player]:
        players: list[Player] = []

        if settings.mode == "pvp":
            human_players = [
                HumanPlayer("Игрок 1", "X"),
                HumanPlayer("Игрок 2", "O"),
            ]
            players.extend(human_players)
        elif settings.mode == "pve":
            players.append(HumanPlayer("Игрок", "X"))

            if settings.difficulty == "easy":
                players.append(RandomAIPlayer("Компьютер", "O"))
            elif settings.difficulty == "normal":
                players.append(
                    HeuristicAIPlayer("Компьютер", "O", settings.line_length)
                )
            elif settings.difficulty == "medium":
                players.append(
                    MinimaxAIPlayer("Компьютер", "O", settings.line_length)
                )
            elif settings.difficulty == "hard":
                players.append(RandomAIPlayer("Компьютер", "O"))  # TODO: Заменить на ML
            else:
                raise ValueError(f"Неизвестная сложность игры: {settings.difficulty}")
        else:
            raise ValueError(f"Неизвестный режим игры: {settings.mode}")

        return players


class HumanPlayer(Player):
    def __init__(self, name: str, symbol: str, score: int = 0) -> None:
        super().__init__(name, symbol, score)

    def make_move(self, board: Board, ui: UI) -> bool:
        cursor_pos = 0
        sqrt_size = int(board.board_size**0.5)

        while True:
            ui.show_board(board, cursor_pos, self.symbol)

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


class AIPlayer(Player, ABC):
    def __init__(self, name: str, symbol: str, score: int = 0) -> None:
        super().__init__(name, symbol, score)


class RandomAIPlayer(AIPlayer):
    def __init__(self, name: str, symbol: str, score: int = 0) -> None:
        super().__init__(name, symbol, score)

    def make_move(self, board: Board, ui: UI) -> bool:
        positions = [randint(0, board.board_size - 1) for _ in range(3)]
        ui.show_ai_thinking(board, positions, self.symbol)

        while True:
            cursor_pos = randint(0, board.board_size - 1)

            if board.is_valid_cell(cursor_pos):
                board.update_value_list(cursor_pos, self.symbol)
                return True


class HeuristicAIPlayer(AIPlayer):
    def __init__(
        self, name: str, symbol: str, line_length: int, score: int = 0
    ) -> None:
        super().__init__(name, symbol, score)
        self.line_length = line_length

    def make_move(self, board: Board, ui: UI) -> bool:
        cursor_pos = self._calculate_next_move(board)
        positions = [_ for _ in range(cursor_pos)]
        ui.show_ai_thinking(board, positions, self.symbol, 0.1)

        while True:
            if not board.is_valid_cell(cursor_pos):
                cursor_pos = self._calculate_next_move(board)
                continue

            board.update_value_list(cursor_pos, self.symbol)
            return True

    def _calculate_next_move(self, board: Board) -> int:
        empty_cells = [i for i, cell in enumerate(board.value_list) if cell == " "]
        enemy_symbol = " "
        best_move = -1

        for symbol in board.value_list:
            if symbol not in (" ", self.symbol):
                enemy_symbol = symbol
                break

        for i in empty_cells:
            if not board.is_valid_cell(i):
                continue

            board.update_value_list(i, self.symbol)

            if not board.is_win(self.symbol, self.line_length):
                for j in empty_cells:
                    if j == i or not board.is_valid_cell(j):
                        continue

                    board.update_value_list(j, enemy_symbol)

                    if board.is_win(enemy_symbol, self.line_length):
                        board.update_value_list(j, " ")
                        best_move = j
                        break

                    board.update_value_list(j, " ")
            else:
                board.update_value_list(i, " ")
                best_move = i
                break

            board.update_value_list(i, " ")

        if best_move == -1:
            while True:
                best_move = randint(0, board.board_size - 1)

                if board.is_valid_cell(best_move):
                    break

        return best_move


class MinimaxAIPlayer(AIPlayer): # TODO: В разработке
    def __init__(
            self, name: str, symbol: str, line_length: int, score: int = 0, max_depth: int = 5
        ) -> None:
        super().__init__(name, symbol, score)
        self.line_length = line_length
        self.max_depth = max_depth

    def make_move(self, board: Board, ui: UI) -> bool:
        cursor_pos = self._calculate_next_move(board)
        positions = [_ for _ in range(cursor_pos)]
        ui.show_ai_thinking(board, positions, self.symbol, 0.1)

        while True:
            if not board.is_valid_cell(cursor_pos):
                return False

            board.update_value_list(cursor_pos, self.symbol)
            return True

    def evaluate(self, board: Board) -> int:
        enemy_symbol = self.get_enemy_symbol(board)
        result = 0

        if board.is_win(self.symbol, self.line_length):
            result = 10
        elif board.is_win(enemy_symbol, self.line_length):
            result = -10
        elif board.is_full():
            result = 0

        return result

    def _calculate_next_move(self, board: Board) -> int:
        empty_cells = self.get_empty_cells(board)
        best_move = -1
        best_value = float("-inf")

        for i in empty_cells:
            board.update_value_list(i, self.symbol)
            value = self._minimax(board, 1, False)
            board.update_value_list(i, " ")

            if value > best_value:
                best_value = value
                best_move = i

        return best_move

    def _minimax(self, board: Board, depth: int, is_maximizing: bool) -> int:
        score = self.evaluate(board)
        if score != 0 or board.is_full():
            return score

        if depth >= self.max_depth:
            return self.evaluate(board)

        if is_maximizing:
            best = float("-inf")
        else:
            best = float("inf")

        empty_cells = self.get_empty_cells(board)
        enemy_symbol = self.get_enemy_symbol(board)

        if is_maximizing:
            for cell in empty_cells:
                board.update_value_list(cell, self.symbol)
                value = self._minimax(board, depth+1, False)
                board.update_value_list(cell, " ")
                best = max(best, value)
        else:
            for cell in empty_cells:
                board.update_value_list(cell, enemy_symbol)
                value = self._minimax(board, depth+1, True)
                board.update_value_list(cell, " ")
                best = min(best, value)

        return int(best)

    def get_empty_cells(self, board: Board) -> list[int]:
        empty_cells = [i for i, cell in enumerate(board.value_list) if cell == " "]
        return empty_cells

    def get_enemy_symbol(self, board: Board) -> str:
        enemy_symbol = "X"

        for symbol in board.value_list:
            if symbol not in (" ", self.symbol):
                enemy_symbol = symbol
                break

        return enemy_symbol
