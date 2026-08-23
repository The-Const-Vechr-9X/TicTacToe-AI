import curses
from src.core.game import Game


def main(stdscr: curses.window):
    game = Game()
    game.show_main_menu(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)
