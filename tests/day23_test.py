import os
from collections import deque
from time import time
from typing import Deque, Dict, Generator, List, Set, Tuple


import pytest

from ..day23.cups import play_cups, part1_with_dict, long_game_of_cups


@pytest.fixture
def cups_input() -> str:
    """
    Returns original set of cups as a string.
    """
    return "389125467"


def test_play_cups(cups_input: str):
    """
    Tests the `play_cups` function.
    """
    cups: Deque[int] = deque([int(num) for num in cups_input])
    final: str = play_cups(cups)
    assert final == "67384529"


def test_part1_with_dict(cups_input: str):
    """
    Tests the `part1_with_dict` function.
    """
    cups: Deque[int] = deque([int(num) for num in cups_input])
    final: str = play_cups(cups)
    assert final == "67384529"


def test_long_game_of_cups(cups_input: str):
    """
    Tests the `long_game_of_cups` function.
    """
    final: str = long_game_of_cups(cups_input)
    assert final == "149245887792"
