from typing import List

import pytest

from ..day2.count import process_password, updated_password_check


@pytest.fixture
def input_list() -> List[str]:
    """
    Returns the test list of passwords.
    """
    return ["1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc"]


def test_process_password(input_list: List[str]):
    """
    Tests if the process_password function works correctly.
    """
    valid: int = 0
    for password in input_list:
        valid += process_password(password)
    assert valid == 2


def test_updated_password_check(input_list: List[str]):
    """
    Tests if the updated_password_check function works correctly.
    """
    valid: int = 0
    for password in input_list:
        valid += updated_password_check(password)
    assert valid == 1
