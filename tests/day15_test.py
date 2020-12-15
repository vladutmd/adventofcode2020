import os
from contextlib import contextmanager
from typing import IO, ContextManager, Dict, Generator, List

import pytest

from ..day15.play import file_read, play_game


@pytest.fixture
def starting_numbers() -> List[List[int]]:
    """
    Returns a list of test input lists..
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day15")
    with cm as input_file:
        starting_numbers: List[List[int]] = [
            [int(num) for num in array.split(",")] for array in input_file.readlines()
        ]
    return starting_numbers


def test_play_game_0(starting_numbers: List[List[int]]):
    """
    This tests the `play_game` function for the 0th test input.
    """
    assert (play_game(starting_numbers[0], 10)) == 0
    assert (play_game(starting_numbers[0], 2020)) == 436
    assert (play_game(starting_numbers[0], 30000000)) == 175594


def test_play_game_1(starting_numbers: List[List[int]]):
    """
    This tests the `play_game` function for the 1st test input.
    """
    assert (play_game(starting_numbers[1], 2020)) == 1
    assert (play_game(starting_numbers[1], 30000000)) == 2578


def test_play_game_2(starting_numbers: List[List[int]]):
    """
    This tests the `play_game` function for the 2nd test input.
    """
    assert (play_game(starting_numbers[2], 2020)) == 10
    assert (play_game(starting_numbers[2], 30000000)) == 3544142


def test_play_game_3(starting_numbers: List[List[int]]):
    """
    This tests the `play_game` function for the 3rd test input.
    """
    assert (play_game(starting_numbers[3], 2020)) == 27
    assert (play_game(starting_numbers[3], 30000000)) == 261214


def test_play_game_4(starting_numbers: List[List[int]]):
    """
    This tests the `play_game` function for the 4th test input.
    """
    assert (play_game(starting_numbers[4], 2020)) == 78
    assert (play_game(starting_numbers[4], 30000000)) == 6895259


def test_play_game_5(starting_numbers: List[List[int]]):
    """
    This tests the `play_game` function for the 5th test input.
    """
    assert (play_game(starting_numbers[5], 2020)) == 438
    assert (play_game(starting_numbers[5], 30000000)) == 18


def test_play_game_6(starting_numbers: List[List[int]]):
    """
    This tests the `play_game` function for the 6th test input.
    """
    assert (play_game(starting_numbers[6], 2020)) == 1836
    assert (play_game(starting_numbers[6], 30000000)) == 362
