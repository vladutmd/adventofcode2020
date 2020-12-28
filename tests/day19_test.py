import os
import re
from contextlib import contextmanager
from typing import IO, ContextManager, Dict, Generator, List, Tuple, Union

import pytest

from ..day19.check import (
    file_read,
    parse_line,
    parse_rules,
    parse_rules_2,
    validate_message,
)


@pytest.fixture
def complete_rules_and_messages() -> Tuple[Dict[str, str], List[str]]:
    """
    Returns the rules and messages for part 1.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day19_1")
    raw_rules: Dict[str, str] = {}
    messages: List[str] = []
    processed: Union[Dict[str, str], str]
    with cm as input_file:
        for line in input_file.read().splitlines():
            processed = parse_line(line)
            if isinstance(processed, dict):
                raw_rules.update(processed)
            elif isinstance(processed, str):
                messages.append(processed)
    complete_rules: Dict[str, str] = parse_rules_2(raw_rules)
    return (complete_rules, messages)


@pytest.fixture
def complete_rules_and_messages_2() -> Tuple[Dict[str, str], List[str]]:
    """
    Returns the rules and messages for part 2.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day19_2")
    raw_rules: Dict[str, str] = {}
    messages: List[str] = []
    processed: Union[Dict[str, str], str]
    with cm as input_file:
        for line in input_file.read().splitlines():
            processed = parse_line(line)
            if isinstance(processed, dict):
                raw_rules.update(processed)
            elif isinstance(processed, str):
                messages.append(processed)
    complete_rules: Dict[str, str] = parse_rules(raw_rules)
    return (complete_rules, messages)


def test_parse_rules_1(complete_rules_and_messages: Tuple[Dict[str, str], List[str]]):
    """
    Tests the `parse_rules` function for part 1.
    """
    complete_rules: Dict[str, str]
    messages: List[str]
    complete_rules, messages = complete_rules_and_messages
    rule_0: str = complete_rules["0"]
    assert sum([validate_message(message, rule_0) for message in messages]) == 2


# def test_parse_rules_2(complete_rules_and_messages_2: Tuple[Dict[str, str], List[str]]):
#     """
#     Tests the `parse_rules` function for part 2.
#     """
#     complete_rules_2: Dict[str, str]
#     messages: List[str]
#     complete_rules_2, messages = complete_rules_and_messages_2
#     rule_0 = complete_rules_2["0"].replace("x", "1")
#     count: int = sum([validate_message(message, rule_0) for message in messages])
#     prev: int = 0
#     rep: int = 2
#     while prev != count:
#         prev = count
#         rule_0 = complete_rules_2["0"].replace("x", str(rep))
#         count += sum([validate_message(message, rule_0) for message in messages])
#         rep += 1
#     assert count == 12
