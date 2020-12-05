from contextlib import contextmanager
from typing import IO, ContextManager, Generator, List

import pytest

from board import decode_pass


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


@pytest.fixture
def boarding_passes() -> List[str]:
    """
    Returns the test input.
    """
    cm: ContextManager[IO] = file_read("testinput")
    with cm as input_file:
        boarding_passes: List[str] = input_file.read().splitlines()
    return boarding_passes


@pytest.fixture
def boarding_pass_ids() -> List[int]:
    """
    Returns the seat ids of the test boarding passes.
    """
    return [357, 567, 119, 820]


def test_pass_decode(boarding_passes: List[str], boarding_pass_ids: List[int]):
    """
    Tests if the decode_pass function works correctly.
    """
    for b_pass, b_pass_id in zip(boarding_passes, boarding_pass_ids):
        assert decode_pass(b_pass) == b_pass_id
