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
