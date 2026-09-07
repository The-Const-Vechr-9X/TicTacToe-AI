import curses

from src.core.game import Game
from src.core.settings import Settings
from src.ui.base import UI
from src.ui.curses_ui import CursesUI

UI_TYPE = "curses"


def create_ui(stdscr: curses.window | None = None) -> UI | None:
    if UI_TYPE == "curses" and stdscr:
        return CursesUI(stdscr)
    return None


def main(stdscr: curses.window) -> None:
    ui = create_ui(stdscr)
    settings = Settings()
    game = Game(settings)

    if ui:
        game.show_main_menu(ui)


if __name__ == "__main__":
    curses.wrapper(main)
