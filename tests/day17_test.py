import os
from collections import defaultdict
from contextlib import contextmanager
from typing import (IO, ContextManager, DefaultDict, Dict, Generator, List,
                    Tuple)

import pytest

from ..day17.simulate import evolve_hyperstate, evolve_state, file_read


@pytest.fixture
def initial_state() -> DefaultDict[Tuple[int, int, int], str]:
    """
    Returns the initial (3d) input.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day17")
    with cm as input_file:
        positions: List[List[str]] = [
            [position for position in line] for line in input_file.read().splitlines()
        ]
    space_map: DefaultDict[Tuple[int, int, int], str] = defaultdict(lambda: ".")
    for i, row in enumerate(positions):
        for j, cube in enumerate(row):
            space_map[i, j, 0] = cube
    return space_map


@pytest.fixture
def initial_hyper_state() -> DefaultDict[Tuple[int, int, int, int], str]:
    """
    Returns the initial (4d) input.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day17")
    with cm as input_file:
        positions: List[List[str]] = [
            [position for position in line] for line in input_file.read().splitlines()
        ]
    hyper_space_map: DefaultDict[Tuple[int, int, int, int], str] = defaultdict(
        lambda: "."
    )
    for i, row in enumerate(positions):
        for j, cube in enumerate(row):
            hyper_space_map[i, j, 0, 0] = cube
    return hyper_space_map


def test_evolve_state(initial_state: DefaultDict[Tuple[int, int, int], str]):
    """
    Tests the `evolve_state` function.
    """
    evolve_state(initial_state, 6)
    count: int = 0
    for cube in initial_state.values():
        if cube == "#":
            count += 1
    assert count == 112


def test_evolve_hyperstate(
    initial_hyper_state: DefaultDict[Tuple[int, int, int, int], str]
):
    """
    Tests the `evolve_hyperstate` function.
    """
    evolve_hyperstate(initial_hyper_state, 6)
    count: int = 0
    for cube in initial_hyper_state.values():
        if cube == "#":
            count += 1
    assert count == 848
