import os
from collections import defaultdict
from contextlib import contextmanager
from typing import (IO, ContextManager, DefaultDict, Dict, Generator, List,
                    Tuple)

import pytest

from ..day11.simulate import swap_diagonal_seats, swap_seats


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


@pytest.fixture
def seat_map() -> Dict[Tuple[int, int], str]:
    """
    Returns the test input 1.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day11")
    with cm as input_file:
        positions: List[List[str]] = [
            [position for position in line] for line in input_file.read().splitlines()
        ]
    pos_dict: Dict[Tuple[int, int], str] = {}
    for i, row in enumerate(positions):
        for j, seat in enumerate(row):
            pos_dict[i, j] = seat
    return pos_dict


def test_swap_seats(seat_map: Dict[Tuple[int, int], str]):
    """
    This functions tests the `swap_seats` function.
    """
    swap_seats(seat_map)
    count: int = 0
    for seat in seat_map.values():
        if seat == "#":
            count += 1
    assert count == 37


def test_swap_diagonal_seats(seat_map: Dict[Tuple[int, int], str]):
    """
    This functions tests the `swap_diagonal_seats` function.
    """
    swap_diagonal_seats(seat_map)
    count: int = 0
    for seat in seat_map.values():
        if seat == "#":
            count += 1
    assert count == 26
