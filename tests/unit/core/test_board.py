from typing import Any

import pytest

from src.core.board import Board

FILLED_BOARD = [" ", "X", "O", " ", "O", "X", "X", " ", "O"]
FIRST_FILLED_BOARD = ["X", "X", "O", " ", "O", "X", "X", " ", "O"]
LAST_EMPTY_BOARD = [" ", "X", "O", " ", "O", "X", "X", " ", " "]
FULL_BOARD = ["X", "X", "O", "O", "O", "X", "X", "X", "O"]
EMPTY_BOARD = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
ONE_FILLED_BOARD = [" ", " ", " ", " ", "X", " ", " ", " ", " "]
ONE_EMPTY_BOARD = ["X", "X", "O", "O", "O", "X", " ", "X", "O"]
X_WIN_HORIZONTAL_BOARD = ["X", "X", "X", " ", "O", " ", "O", " ", "O"]
X_WIN_VERTICAL_BOARD = ["X", "O", "O", "X", "O", " ", "X", " ", "O"]
X_WIN_DIAGONAL_LEFT_CORNER_BOARD = ["X", "O", "O", " ", "X", "O", " ", "O", "X"]
X_WIN_DIAGONAL_RIGHT_CORNER_BOARD = [" ", "O", "X", "O", "X", " ", "X", "O", "O"]
O_WIN_HORIZONTAL_BOARD = ["X", " ", "X", " ", "X", " ", "O", "O", "O"]
O_WIN_VERTICAL_BOARD = ["X", "X", "O", " ", "X", "O", "X", " ", "O"]
O_WIN_DIAGONAL_LEFT_CORNER_BOARD = ["O", "X", "X", " ", "O", "X", " ", "X", "O"]
O_WIN_DIAGONAL_RIGHT_CORNER_BOARD = [" ", "X", "O", "X", "O", " ", "O", "X", "X"]
X_AND_O_WIN_DIAGONAL_BOARD_4X4 = [
    "O",
    "X",
    " ",
    " ",
    " ",
    "O",
    "X",
    " ",
    " ",
    " ",
    "O",
    "X",
    " ",
    " ",
    " ",
    "O",
]
X_AND_O_WIN_DIAGONAL_BOARD_5X5 = [
    " ",
    " ",
    " ",
    " ",
    "X",
    " ",
    " ",
    " ",
    "X",
    "O",
    " ",
    " ",
    "X",
    "O",
    " ",
    " ",
    "X",
    "O",
    " ",
    " ",
    "X",
    "O",
    " ",
    " ",
    " ",
]


@pytest.fixture
def board() -> Board:
    return Board()


@pytest.mark.parametrize(
    "value_list, index_cell, expected",
    [
        (FILLED_BOARD, 3, True),
        (FILLED_BOARD, 5, False),
        (FILLED_BOARD, 0, True),
        (FIRST_FILLED_BOARD, 0, False),
        (LAST_EMPTY_BOARD, 8, True),
        (FILLED_BOARD, 8, False),
    ],
    ids=[
        "middle-empty",
        "middle-filled",
        "first-empty",
        "first-filled",
        "last-empty",
        "last-filled",
    ],
)
def test_is_valid_cell(
    board: Board, value_list: list[str], index_cell: int, expected: bool
) -> None:
    board.value_list = value_list

    assert board.is_valid_cell(index_cell) == expected


@pytest.mark.parametrize(
    "index_cell, exc",
    [
        (-1, IndexError),
        (9, IndexError),
        (2.5, TypeError),
        ("2", TypeError),
        (["something", None], TypeError),
        ({"bool": False}, TypeError),
        (None, TypeError),
        (True, TypeError),
        (False, TypeError),
    ],
    ids=[
        "negative-index",
        "out-of-range",
        "float",
        "numeric-string",
        "list",
        "dict",
        "none",
        "bool-true",
        "bool-false",
    ],
)
def test_is_valid_cell_raises(
    board: Board, index_cell: Any, exc: type[Exception]
) -> None:
    board.value_list = FILLED_BOARD

    with pytest.raises(exc):
        board.is_valid_cell(index_cell)


@pytest.mark.parametrize(
    "value_list, expected",
    [
        (FILLED_BOARD, False),
        (FULL_BOARD, True),
        (EMPTY_BOARD, False),
        (ONE_FILLED_BOARD, False),
        (ONE_EMPTY_BOARD, False),
    ],
    ids=["filled", "full", "empty", "one-filled", "one-empty"],
)
def test_is_full(board: Board, value_list: list[str], expected: bool) -> None:
    board.value_list = value_list

    assert board.is_full() == expected


@pytest.mark.parametrize(
    "value_list, symbol, line_length, expected",
    [
        (FILLED_BOARD, "X", 3, False),
        (FILLED_BOARD, "O", 3, False),
        (X_WIN_HORIZONTAL_BOARD, "X", 3, True),
        (X_WIN_HORIZONTAL_BOARD, "O", 3, False),
        (X_WIN_VERTICAL_BOARD, "X", 3, True),
        (X_WIN_VERTICAL_BOARD, "O", 3, False),
        (X_WIN_DIAGONAL_LEFT_CORNER_BOARD, "X", 3, True),
        (X_WIN_DIAGONAL_LEFT_CORNER_BOARD, "O", 3, False),
        (X_WIN_DIAGONAL_RIGHT_CORNER_BOARD, "X", 3, True),
        (X_WIN_DIAGONAL_RIGHT_CORNER_BOARD, "O", 3, False),
        (O_WIN_HORIZONTAL_BOARD, "O", 3, True),
        (O_WIN_HORIZONTAL_BOARD, "X", 3, False),
        (O_WIN_VERTICAL_BOARD, "O", 3, True),
        (O_WIN_VERTICAL_BOARD, "X", 3, False),
        (O_WIN_DIAGONAL_LEFT_CORNER_BOARD, "O", 3, True),
        (O_WIN_DIAGONAL_LEFT_CORNER_BOARD, "X", 3, False),
        (O_WIN_DIAGONAL_RIGHT_CORNER_BOARD, "O", 3, True),
        (O_WIN_DIAGONAL_RIGHT_CORNER_BOARD, "X", 3, False),
        (X_AND_O_WIN_DIAGONAL_BOARD_4X4, "X", 3, True),
        (X_AND_O_WIN_DIAGONAL_BOARD_4X4, "O", 4, True),
        (X_AND_O_WIN_DIAGONAL_BOARD_4X4, "O", 3, True),
        (X_AND_O_WIN_DIAGONAL_BOARD_5X5, "X", 5, True),
        (X_AND_O_WIN_DIAGONAL_BOARD_5X5, "O", 4, True),
    ],
    ids=[
        "x-not-win-filled",
        "o-not-win-filled",
        "x-win-horizontal",
        "o-not-win-horizontal",
        "x-win-vertical",
        "o-not-win-vertical",
        "x-win-diagonal-left-corner",
        "o-not-win-diagonal-left-corner",
        "x-win-diagonal-right-corner",
        "o-not-win-diagonal-right-corner",
        "o-win-horizontal",
        "x-not-win-horizontal",
        "o-win-vertical",
        "x-not-win-vertical",
        "o-win-diagonal-left-corner",
        "x-not-win-diagonal-left-corner",
        "o-win-diagonal-right-corner",
        "x-not-win-diagonal-right-corner",
        "x-win-diagonal-4x4-line-length-3",
        "o-win-diagonal-4x4-line-length-4",
        "o-win-diagonal-4x4-line-length-3",
        "x-win-diagonal-5x5-line-length-5",
        "o-win-diagonal-5x5-line-length-4",
    ],
)
def test_is_win(
    board: Board, value_list: list[str], symbol: str, line_length: int, expected: bool
) -> None:
    board.board_size = len(value_list)
    board.value_list = value_list

    assert board.is_win(symbol, line_length) == expected
