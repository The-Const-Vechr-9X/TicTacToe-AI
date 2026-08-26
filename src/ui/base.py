from abc import ABC, abstractmethod

from src.core.board import Board


class UI(ABC):
    @abstractmethod
    def show_board(self, board: Board, cursor_pos: int) -> None: pass
    @abstractmethod
    def show_menu(self, options: list[str], title: str, cursor_pos: int) -> None: pass
    @abstractmethod
    def show_message(self, text: str) -> None: pass
    @abstractmethod
    def get_key(self) -> str: pass
