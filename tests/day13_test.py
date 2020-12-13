import os
from contextlib import contextmanager
from math import prod
from typing import IO, ContextManager, Dict, Generator, List, Tuple

import pytest

from ..day13.bus import (find_earliest_bus,
                         find_first_timestamp_matching_offsets)


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


@pytest.fixture
def bus_times_1() -> Tuple[int, List[int]]:
    """
    Returns the test input 1.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day13_1")
    with cm as input_file:
        time: int = int(input_file.readline())
        buses: List[str] = [bus for bus in input_file.readline().split(",")]
    real_buses: List[int] = [int(bus) for bus in buses if bus != "x"]
    return (time, real_buses)


@pytest.fixture
def bus_times_2() -> List[Tuple[int, int]]:
    """
    Returns the test input 2.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day13_2")
    with cm as input_file:
        buses: List[str] = [bus for bus in input_file.readline().split(",")]
    bus_offset: List[Tuple[int, int]] = [
        (offset, int(bus)) for offset, bus in enumerate(buses) if bus != "x"
    ]
    return bus_offset


def test_find_earliest_bus(bus_times_1: Tuple[int, List[int]]):
    """
    This tests the `find_earliest_bus` function.
    """
    time, real_buses = bus_times_1
    assert prod(find_earliest_bus(time, real_buses)) == 295


def test_find_first_timestamp_matching_offsets(bus_times_2: List[Tuple[int, int]]):
    """
    This tests the `find_first_timestamp_matching_offsets` function.
    """
    assert find_first_timestamp_matching_offsets(bus_times_2) == 1068781
