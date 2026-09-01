from src.ui.base import UI

from .board import Board
from .player import HumanPlayer


class Game:
    def __init__(self) -> None:
        self.players = [HumanPlayer("Игрок 1", "X"), HumanPlayer("Игрок 2", "O")]
        self.current_player_index = 0
        self.settings: dict[str, int | str] = {
            "board_size": 9,
            "mode": "pvp",
            "difficulty": "medium",
        }

    def show_main_menu(self, ui: UI) -> None:
        again = False
        cursor_pos = 1
        menu_options = ["Играть", "Настройки", "Выход"]

        while True:
            if again == True:
                self.play(ui)
                again = self.play_again(ui)
                continue

            ui.show_menu(menu_options, "Крестики-нолики", cursor_pos)

            key = ui.get_key()

            if key == "q" or key == "escape":
                break
            elif key == "confirm":
                if cursor_pos == 1:
                    self.play(ui)
                    again = self.play_again(ui)
                elif cursor_pos == 2:
                    self.show_settings(ui)
                elif cursor_pos == 3:
                    break
            else:
                cursor_pos = self._move_menu_cursor(key, cursor_pos, menu_options)

    def show_settings(self, ui: UI) -> None:
        ui.show_message(str(self.settings))

    def _move_menu_cursor(self, key: str, cursor_pos: int, menu_options: list[str]) -> int:
        if key == "up" and cursor_pos > 1:
            cursor_pos -= 1
        elif key == "down" and cursor_pos < len(menu_options):
            cursor_pos += 1

        return cursor_pos

    def play(self, ui: UI) -> None:
        self.board = Board()
        self.current_player_index = 0

        while True:
            current = self.players[self.current_player_index]
            current.make_move(self.board, ui)
            # BUG: Если нажать Q, то игрок может пропустить свой ход.

            if self.board.is_win(current.symbol):
                self.show_winner(ui, current)
                break

            if self.board.is_full():
                self.show_draw(ui)
                break

            self.current_player_index = 1 - self.current_player_index

    def play_again(self, ui: UI) -> bool:
        cursor_pos = 1
        menu_options = ["Да", "Нет"]

        while True:
            ui.show_menu(menu_options, "Желаете сыграть снова?", cursor_pos)
            key = ui.get_key()

            if key == "confirm":
                if cursor_pos == 1:
                    return True
                elif cursor_pos == 2:
                    return False
            else:
                cursor_pos = self._move_menu_cursor(key, cursor_pos, menu_options)

    def show_winner(self, ui: UI, player: HumanPlayer) -> None:
        ui.show_message(
            f"Победил {player.name} ({player.symbol})!\nНажмите любую кнопку для продолжения."
        )

    def show_draw(self, ui: UI) -> None:
        ui.show_message("Ничья!\nНажмите любую кнопку для продолжения.")
