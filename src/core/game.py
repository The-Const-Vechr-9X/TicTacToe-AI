from src.ui.curses_ui import CursesUI

from .board import Board
from .player import HumanPlayer


class Game:
    def __init__(self) -> None:
        self.players = [HumanPlayer("Игрок 1", "X"), HumanPlayer("Игрок 2", "O")]
        self.current_player_index = 0
        self.running = True
        self.menu_options = ["Играть", "Настройки"]
        self.settings: dict[str, int | str] = {
            "board_size": 9,
            "mode": "pvp",
            "difficulty": "medium",
        }

    def show_main_menu(self, ui: CursesUI) -> None:
        cursor_pos = 1
        again = False

        while self.running:
            if again == True:
                self.play(ui)
                again = self.play_again(ui)
                continue

            ui.show_menu(self.menu_options, "Крестики-нолики", cursor_pos)

            key = ui.get_key()

            if key == "q":
                self.running = False
                break
            elif key == "confirm":
                if cursor_pos == 1:
                    self.play(ui)
                    again = self.play_again(ui)
                    continue
                elif cursor_pos == 2:
                    self.show_settings(ui)
            else:
                cursor_pos = self._move_menu_cursor(key, cursor_pos)

    def show_settings(self, ui: CursesUI) -> None:
        pass

    def _move_menu_cursor(self, key: str, cursor_pos: int) -> int:
        if key == "up":
            if cursor_pos > 1:
                cursor_pos -= 1
        elif key == "down":
            if cursor_pos < len(self.menu_options):
                cursor_pos += 1

        return cursor_pos

    def play(self, ui: CursesUI) -> None:
        self.board = Board()
        self.current_player_index = 0

        while True:
            current = self.players[self.current_player_index]
            current.make_move(self.board, ui)

            if self.board.is_win(current.symbol):
                self.show_winner(ui, current)
                break

            if self.board.is_full():
                self.show_draw(ui)
                break

            self.current_player_index = 1 - self.current_player_index

    def play_again(self, ui: CursesUI) -> bool:
        cursor_pos = 1

        while True:
            ui.show_menu(["Да", "Нет"], "Желаете сыграть снова?", cursor_pos)
            key = ui.get_key()

            if key == "confirm":
                if cursor_pos == 1:
                    return True
                elif cursor_pos == 2:
                    return False
            else:
                cursor_pos = self._move_menu_cursor(key, cursor_pos)

    def show_winner(self, ui: CursesUI, player: HumanPlayer) -> None:
        ui.show_message(
            f"Победил {player.name}!\nНажмите любую кнопку для продолжения."
        )

    def show_draw(self, ui: CursesUI) -> None:
        ui.show_message("Ничья!\nНажмите любую кнопку для продолжения.")
