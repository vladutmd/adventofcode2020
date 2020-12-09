import os
import re
from contextlib import contextmanager
from typing import (IO, ContextManager, DefaultDict, Deque, Generator, List,
                    Match, Optional, Set, Tuple)

import pytest

from ..day7.bags import how_many_bags, how_many_colours_contain, process_rules


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


@pytest.fixture
def bags_part1() -> Tuple[
    DefaultDict[str, List[Tuple[int, str]]], DefaultDict[str, Set[str]]
]:
    """
    Returns the test input for part 1.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day7_1")
    with cm as input_file:
        rules: List[str] = input_file.read().splitlines()
    has, isin = process_rules(rules)
    return (has, isin)


@pytest.fixture
def bags_part2() -> Tuple[
    DefaultDict[str, List[Tuple[int, str]]], DefaultDict[str, Set[str]]
]:
    """
    Returns the test input for part 2.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day7_2")
    with cm as input_file:
        rules: List[str] = input_file.read().splitlines()
    has, isin = process_rules(rules)
    return (has, isin)


def test_process_rules():
    """
    Tests if the process_rules functions works correctly.
    """
    rule1: str = "light red bags contain 1 bright white bag, 2 muted yellow bags."
    has, isin = process_rules([rule1])
    assert has == {"light red": [(1, "bright white"), (2, "muted yellow")]}
    assert isin == {"bright white": {"light red"}, "muted yellow": {"light red"}}
    rule2: str = "dark orange bags contain 3 bright white bags, 4 muted yellow bags."
    has, isin = process_rules([rule2])
    assert has == {"dark orange": [(3, "bright white"), (4, "muted yellow")]}
    assert isin == {"bright white": {"dark orange"}, "muted yellow": {"dark orange"}}
    rule3: str = "dotted black bags contain no other bags."
    has, isin = process_rules([rule3])
    assert has == {}
    assert isin == {}


def test_how_many_colours_contain():
    """
    This functions tests the how_many_colours_contain function.
    """
    pass
    # (has, isin) = bags_part1

    # assert how_many_colours_contain(has, isin, 'shiny gold') == 4
