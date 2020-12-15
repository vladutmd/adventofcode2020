import os
from collections import defaultdict
from contextlib import contextmanager
from typing import (
    IO,
    ContextManager,
    DefaultDict,
    Dict,
    Generator,
    List,
    Optional,
    Tuple,
    Union,
)

import pytest

from ..day8.execute import run_program, try_fixing_program


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


@pytest.fixture
def instructions() -> List[List[Union[str, int]]]:
    """
    Returns the test input for both parts.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day8")
    with cm as input_file:
        instructions: List[List[Union[str, int]]] = [
            [line.split()[0], int(line.split()[1])]
            for line in input_file.read().splitlines()
        ]
    return instructions


def test_run_program(instructions: List[List[Union[str, int]]]):
    """
    Tests the `run_program` function.
    """
    acc, _ = run_program(instructions)
    assert acc == 5


def test_fix_program(instructions: List[List[Union[str, int]]]):
    """
    Tests the `try_fixing_program` function.
    """
    acc = try_fixing_program(instructions)
    assert acc == 8
