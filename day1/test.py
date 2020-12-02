from math import prod
from typing import List

import pytest

from search import find_sum_three, find_sum_two


@pytest.fixture
def input_list() -> List[int]:
    """
    Returns the test list of entries.
    """
    return [1721, 979, 366, 299, 675, 1456]


@pytest.fixture
def input_sum() -> int:
    """
    Returns the sum that we are looking for.
    """
    return 2020


def test_sum_two(input_list: List[int], input_sum: int):
    """
    Tests if the sum_two function works correctly.
    """
    two_numbers = find_sum_two(input_list, input_sum)
    two_numbers.sort()
    assert two_numbers == [299, 1721]
    assert prod(two_numbers) == 514579


def test_sum_three(input_list: List[int], input_sum: int):
    """
    Tests if the sum_three function works correctly.
    """
    three_numbers = find_sum_three(input_list, input_sum)
    three_numbers.sort()
    assert three_numbers == [366, 675, 979]
    assert prod(three_numbers) == 241861950
