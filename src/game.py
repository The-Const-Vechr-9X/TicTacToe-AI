from .board import Board
from .player import HumanPlayer
import curses


class Game():
    def __init__(self) -> None:
        self.board = Board()
        self.players = []
        self.current_player_index = 0
        self.running = True
        self.buttons = {
            "play": "Играть",
            "settings": "Настройки"
        }
        self.settings: dict[str, int | str] = {
            "board_size": 9,
            "mode": "pvp",
            "difficulty": "medium"
        }

    def show_main_menu(self, stdscr: curses.window) -> None:
        stdscr.clear()
        curses.curs_set(0)

        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        cursor = 1

        while self.running:

            index = 1

            stdscr.addstr(0, 0, f"TicTacToe-AI", curses.A_BOLD)

            for k in self.buttons:

                if index == cursor:
                    stdscr.addstr(index, 0, " > " + self.buttons[k], curses.color_pair(1))
                else:
                    stdscr.addstr(index, 0, " - " + self.buttons[k])

                index += 1

            stdscr.refresh()
            key = stdscr.getch()

            if key == ord('q'):
                self.running = False
            elif key in (ord('z'), ord('\n')):
                if cursor == 1:
                    self.play(stdscr)
                    stdscr.clear()
                    continue
                elif cursor == 2:
                    self.show_settings(stdscr)
            else:
                cursor = self._move_cursor(key, cursor)

    def show_settings(self, stdscr: curses.window) -> None:
        pass

    def _move_cursor(self, key: int, cursor: int) -> int:
        if key in (curses.KEY_UP, ord('w')):
            if cursor > 1:
                cursor -= 1
        elif key in (curses.KEY_DOWN, ord('s')):
            if cursor < len(self.buttons):
                cursor += 1

        return cursor

    def play(self, stdscr: curses.window) -> None:
        self.players = [
            HumanPlayer("Игрок 1", 'X'),
            HumanPlayer("Игрок 2", 'O')
        ]
        self.current_player_index = 0

        while True:
            current = self.players[self.current_player_index]
            current.make_move(self.board, stdscr)

            if self.board.is_win(current.symbol):
                self.show_winner(stdscr, current)
                break

            if self.board.is_full():
                self.show_draw(stdscr)
                break

            self.current_player_index = 1 - self.current_player_index

        self.board = Board()

    def play_again(self, stdscr: curses.window) -> bool:
        pass

    def show_winner(self, stdscr: curses.window, player: HumanPlayer) -> None:
        stdscr.clear()
        self.board.draw(stdscr)
        stdscr.addstr(10, 0, f"Победил {player.name}!")
        stdscr.refresh()
        stdscr.getch()

    def show_draw(self, stdscr: curses.window) -> None:
        stdscr.clear()
        self.board.draw(stdscr)
        stdscr.addstr(10, 0, "Ничья!")
        stdscr.refresh()
        stdscr.getch()
