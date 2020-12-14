import os
import re
from collections import defaultdict, deque
from contextlib import contextmanager
from typing import IO, ContextManager, Deque, Dict, Generator, List, Tuple

import pytest

from ..day14.bits import (apply_bitmask, apply_floatmask, file_read,
                          line_processor)


def test_apply_bitmask():
    """
    Tests the `apply_bitmask` function.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    memory_dict: Dict[int, int] = {}
    for instruction in line_processor(dir_path + "/testinputs/day14_1"):
        if isinstance(instruction, str):
            mask: str = instruction
        else:
            address: int = instruction[0]
            value: int = instruction[1]
            memory_dict[address] = apply_bitmask(mask, value)
    assert sum(memory_dict.values()) == 165


def test_apply_floatmask():
    """
    Tests the `apply_floatmask` function.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    new_memory_dict: Dict[int, int] = {}
    for instruction in line_processor(dir_path + "/testinputs/day14_2"):
        if isinstance(instruction, str):
            new_mask: str = instruction
        else:
            new_address: int = instruction[0]
            new_value: int = instruction[1]
            new_addresses = apply_floatmask(new_mask, new_address)
            for new_address in new_addresses:
                new_memory_dict[new_address] = new_value
    assert sum(new_memory_dict.values()) == 208
