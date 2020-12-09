import os
from contextlib import contextmanager
from math import prod
from typing import IO, ContextManager, Generator, List, Tuple

import pytest

from ..day3.trajectory import slide_down


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


@pytest.fixture
def processed_map() -> List[List[int]]:
    """
    Returns the test input.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day3")
    with cm as input_file:
        input_map: List[str] = input_file.read().splitlines()
    processed: List[List[int]] = [[0 if i == "." else 1 for i in j] for j in input_map]
    return processed


def test_slide_slope_once(processed_map: List[List[int]]):
    """
    Tests if the slide_down function works correctly.
    """
    initial_slope: Tuple[int, int] = (3, 1)
    assert slide_down(processed_map, initial_slope) == 7


def test_slide_many_slopes(processed_map: List[List[int]]):
    """
    Tests if the slide_down function works for all slopes.
    """
    slopes: List[Tuple[int, int]] = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    assert prod([slide_down(processed_map, i) for i in slopes]) == 336
