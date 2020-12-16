import os
import re
from collections import defaultdict, deque
from contextlib import contextmanager
from itertools import chain
from typing import IO, ContextManager, Dict, Generator, List, Set, Tuple, ValuesView

import pytest

from ..day16.translate import (
    determine_field_orders,
    line_processor,
    validate_ticket,
    validate_tickets,
)


@pytest.fixture
def starting_tickets_1() -> Tuple[Dict[str, List[Tuple[int, int]]], List[List[int]]]:
    """
    Returns the first test input: tickets and rules_dict.
    """
    rules_dict: Dict[str, List[Tuple[int, int]]] = {}
    tickets: List[List[int]] = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for line in line_processor(dir_path + "/testinputs/day16_1"):
        if isinstance(line, dict):
            rules_dict.update(line)
        else:
            tickets.append(line)
    return (rules_dict, tickets)


@pytest.fixture
def starting_tickets_2() -> Tuple[Dict[str, List[Tuple[int, int]]], List[List[int]]]:
    """
    Returns the first test input: tickets and rules_dict.
    """
    rules_dict: Dict[str, List[Tuple[int, int]]] = {}
    tickets: List[List[int]] = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for line in line_processor(dir_path + "/testinputs/day16_2"):
        if isinstance(line, dict):
            rules_dict.update(line)
        else:
            tickets.append(line)
    return (rules_dict, tickets)


def test_validate_ticket(
    starting_tickets_1: Tuple[Dict[str, List[Tuple[int, int]]], List[List[int]]]
):
    """
    Tests the `validate_ticket` function.
    """
    rules_dict, tickets = starting_tickets_1
    sum_num: int = 0
    _ = tickets.pop(0)
    for ticket in tickets:
        sum_num += validate_ticket(ticket, rules_dict.values())
    assert sum_num == 71


def test_determine_field_orders(
    starting_tickets_2: Tuple[Dict[str, List[Tuple[int, int]]], List[List[int]]]
):
    """
    Tests the `determine_field_orders` function.
    """
    rules_dict, tickets = starting_tickets_2
    _ = tickets.pop(0)
    valid_tickets = validate_tickets(tickets, rules_dict)
    map_dict = determine_field_orders(valid_tickets, rules_dict)
    assert map_dict == {"row": 0, "class": 1, "seat": 2}
