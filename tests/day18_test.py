import os
import re
from contextlib import contextmanager
from typing import IO, ContextManager, Generator, List

import pytest

from ..day18.math import file_read, parse_equation


@pytest.fixture
def equations() -> List[str]:
    """
    Returns the test set of equations.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day18")
    with cm as input_file:
        equations: List[str] = [
            equation.replace(" ", "") for equation in input_file.read().splitlines()
        ]
    return equations


def test_parse_equation_1(equations: List[str]):
    """
    Tests the `parse_equation` function with the default operator replacement
    for part 1.
    """
    assert sum(map(parse_equation, equations)) == 26457


def test_parse_equation_2(equations: List[str]):
    """
    Tests the `parse_equation` function with switching operators
    so that addition happens before multiplication.
    """
    assert sum(parse_equation(equation, "&") for equation in equations) == 694173
