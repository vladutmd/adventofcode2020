from contextlib import contextmanager
from typing import IO, ContextManager, Generator, List

import pytest

from customs import count_all_answers, count_answers


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


@pytest.fixture
def groups() -> List[List[str]]:
    """
    Returns the test input.
    """
    cm: ContextManager[IO] = file_read("testinput")
    with cm as input_file:
        groups: List[List[str]] = [
            j
            for j in [
                i.replace("\n", " ").split() for i in input_file.read().split("\n\n")
            ]
        ]
    return groups


def test_count_answers(groups: List[List[str]]):
    """
    This function tests the count_answers function.
    """
    count: int = 0
    for group in groups:
        count += count_answers(group)
    assert count == 11


def test_count_all_answers(groups: List[List[str]]):
    """
    This function tests the count_all_answers function.
    """
    count: int = 0
    for group in groups:
        count += count_all_answers(group)
    assert count == 6
