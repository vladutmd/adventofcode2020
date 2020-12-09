import os
from collections import deque
from contextlib import contextmanager
from typing import IO, ContextManager, Deque, Generator, List

import pytest

from ..day9.crack import break_encryption, process_list


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


@pytest.fixture
def list_1() -> List[int]:
    """
    Returns the test input for part 1.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day9")
    with cm as input_file:
        numbers: List[int] = [int(line) for line in input_file.read().splitlines()]
    return numbers


def test_process_list(list_1: List[int]):
    """
    This tests if the `process_list` function works correctly.
    """
    assert process_list(list_1, 5) == 127


def test_break_encryption(list_1: List[int]):
    """
    This tests if the `break_encryption` function works correctly.
    """
    assert break_encryption(list_1, 127) == 62
