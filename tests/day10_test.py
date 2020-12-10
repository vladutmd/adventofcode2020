import os
from contextlib import contextmanager
from operator import mul, sub
from typing import IO, ContextManager, Dict, Generator, List

import pytest

from ..day10.adapt import (
    calculate_arrangements,
    calculate_differences,
    count_difference_patterns,
    count_differences,
)


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


@pytest.fixture
def adapters_1() -> List[int]:
    """
    Returns the test input 1.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day10_1")
    with cm as input_file:
        adapters: List[int] = [int(line) for line in input_file.read().splitlines()]
    adapters.append(0)
    adapters.append(max(adapters) + 3)
    adapters.sort()
    return adapters


@pytest.fixture
def adapters_2() -> List[int]:
    """
    Returns the test input 2.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day10_2")
    with cm as input_file:
        adapters: List[int] = [int(line) for line in input_file.read().splitlines()]
    adapters.append(0)
    adapters.append(max(adapters) + 3)
    adapters.sort()
    return adapters


def test_calculate_differences_1(adapters_1: List[int]):
    """
    Tests the `calculate_differences` function for test input 1.
    """
    assert calculate_differences(adapters_1) == [1, 3, 1, 1, 1, 3, 1, 1, 3, 1, 3, 3]


def test_calculate_differences_2(adapters_2: List[int]):
    """
    Tests the `calculate_differences` function for test input 1.
    """
    assert calculate_differences(adapters_2) == [
        1,
        1,
        1,
        1,
        3,
        1,
        1,
        1,
        1,
        3,
        3,
        1,
        1,
        1,
        3,
        1,
        1,
        3,
        3,
        1,
        1,
        1,
        1,
        3,
        1,
        3,
        3,
        1,
        1,
        1,
        1,
        3,
    ]


def test_count_differences_1(adapters_1: List[int]):
    """
    Tests the `count_differences` function for test input 1.
    """
    assert count_differences(calculate_differences(adapters_1)) == {1: 7, 3: 5}


def test_count_differences_2(adapters_2: List[int]):
    """
    Tests the `count_differences` function for test input 2.
    """
    assert count_differences(calculate_differences(adapters_2)) == {1: 22, 3: 10}


def test_count_differences_patterns_1(adapters_1: List[int]):
    """
    Tests the `count_differences_patterns` function for test input 1.
    """
    assert count_difference_patterns(calculate_differences(adapters_1)) == {
        2: 1,
        3: 1,
        4: 0,
    }


def test_count_differences_patterns_2(adapters_2: List[int]):
    """
    Tests the `count_differences_patterns` function for test input 2.
    """
    assert count_difference_patterns(calculate_differences(adapters_2)) == {
        2: 1,
        3: 1,
        4: 4,
    }


def test_calculate_arrangements_1(adapters_1: List[int]):
    """
    Tests the `calculate_arrangements` function for test input 1.
    """
    assert (
        calculate_arrangements(
            count_difference_patterns(calculate_differences(adapters_1))
        )
        == 8
    )


def test_calculate_arrangements_2(adapters_2: List[int]):
    """
    Tests the `calculate_arrangements` function for test input 2.
    """
    assert (
        calculate_arrangements(
            count_difference_patterns(calculate_differences(adapters_2))
        )
        == 19208
    )
