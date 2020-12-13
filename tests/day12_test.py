import os
from contextlib import contextmanager
from typing import IO, ContextManager, Dict, Generator, List, Tuple

import pytest

from ..day12.evade import travel, travel_with_waypoint


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


@pytest.fixture
def instructions() -> List[Tuple[str, int]]:
    """
    Returns the test input 1.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day12")
    with cm as input_file:
        instructions: List[Tuple[str, int]] = [
            (line[0], int(line[1:])) for line in input_file.read().splitlines()
        ]
    return instructions


def test_travel_function(instructions: List[Tuple[str, int]]):
    """
    This tests the `travel` function.
    """
    pos, _ = travel(instructions)
    distance: int = abs(pos[0]) + abs(pos[1])
    assert distance == 25


def test_travel_with_waypoint_function(instructions: List[Tuple[str, int]]):
    """
    This tests the `travel_with_waypoint` function.
    """
    pos = travel_with_waypoint(instructions)
    distance: int = abs(pos[0]) + abs(pos[1])
    assert distance == 286
