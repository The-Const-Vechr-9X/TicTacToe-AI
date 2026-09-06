from src.ui.base import UI

from .board import Board
from .player import HumanPlayer, Player, RandomAIPlayer
from .settings import Settings


class Game:
    def __init__(self) -> None:
        self.players: list[Player] = [
            HumanPlayer("Игрок", "X"),
            RandomAIPlayer("Компьютер", "O"),
        ]
        self.current_player_index = 0
        self.play_again_requested = False
        self.settings = Settings()

    def show_main_menu(self, ui: UI) -> None:
        cursor_pos = 0
        menu_options = ["Играть", "Настройки", "Выход"]

        while True:
            if self.play_again_requested:
                self.play(ui)
                if self.play_again_requested:
                    self.play_again_requested = self.ask_play_again(ui)
                    continue

            ui.show_menu(menu_options, "Крестики-нолики", cursor_pos)

            key = ui.get_key()

            if key == "q" or key == "escape":
                break
            elif key == "confirm":
                if cursor_pos == 0:
                    self.play_again_requested = True
                    self.play(ui)
                    if self.play_again_requested:
                        self.play_again_requested = self.ask_play_again(ui)
                elif cursor_pos == 1:
                    self.show_settings(ui)
                elif cursor_pos == 2:
                    break
            else:
                cursor_pos = self._move_menu_cursor(key, cursor_pos, menu_options)

    def show_settings(self, ui: UI) -> None:
        ui.show_message(str(self.settings.to_dict()))

    def _move_menu_cursor(
        self, key: str, cursor_pos: int, menu_options: list[str]
    ) -> int:
        if key == "up" and cursor_pos > 0:
            cursor_pos -= 1
        elif key == "down" and cursor_pos < len(menu_options) - 1:
            cursor_pos += 1

        return cursor_pos

    def play(self, ui: UI) -> None:
        self.board = Board(int(self.settings.board_size))
        self.current_player_index = 0

        while True:
            current = self.players[self.current_player_index]
            if not current.make_move(self.board, ui):
                self.play_again_requested = False
                break

            if self.board.is_win(current.symbol):
                self.show_winner(ui, current)
                break

            if self.board.is_full():
                self.show_draw(ui)
                break

            self.current_player_index = 1 - self.current_player_index

    def ask_play_again(self, ui: UI) -> bool:
        cursor_pos = 0
        menu_options = ["Нет", "Да"]

        while True:
            ui.show_menu(menu_options, "Желаете сыграть снова?", cursor_pos)
            key = ui.get_key()

            if key == "confirm":
                if cursor_pos == 0:
                    return False
                elif cursor_pos == 1:
                    return True
            else:
                cursor_pos = self._move_menu_cursor(key, cursor_pos, menu_options)

    def show_winner(self, ui: UI, player: Player) -> None:
        ui.show_message(
            f"Победил {player.name} ({player.symbol})!\nНажмите любую кнопку для продолжения."
        )

    def show_draw(self, ui: UI) -> None:
        ui.show_message("Ничья!\nНажмите любую кнопку для продолжения.")
