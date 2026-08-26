import curses

from src.core.game import Game
from src.ui.curses_ui import CursesUI


def main(stdscr: curses.window):
    ui = CursesUI(stdscr)
    game = Game()
    game.show_main_menu(ui)


if __name__ == "__main__":
    curses.wrapper(main)
