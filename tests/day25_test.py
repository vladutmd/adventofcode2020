import os
from contextlib import contextmanager
from typing import IO, ContextManager, Generator, List, Tuple

import pytest

from ..day25.unlock import file_read, get_loop_size, transform_subject


@pytest.fixture
def card_door_keys() -> Tuple[int, int]:
    """
    Returns the two keys.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day25")
    with cm as input_file:
        keys: List[int] = [int(line) for line in input_file.read().splitlines()]
    card_pubkey: int = keys[0]
    door_pubkey: int = keys[1]
    return (card_pubkey, door_pubkey)


def test_get_loop_size(card_door_keys: Tuple[int, int]):
    """
    Tests the `get_loop_size` function.
    """
    card_pubkey: int
    door_pubkey: int
    card_pubkey, door_pubkey = card_door_keys
    assert get_loop_size(7, card_pubkey) == 8
    assert get_loop_size(7, door_pubkey) == 11


def test_transform_subject(card_door_keys: Tuple[int, int]):
    """
    Tests the `transform_subject` function.
    """
    card_pubkey: int
    door_pubkey: int
    card_pubkey, door_pubkey = card_door_keys
    card_loop_size: int = get_loop_size(7, card_pubkey)
    door_loop_size: int = get_loop_size(7, door_pubkey)
    door_handshake: int = transform_subject(door_pubkey, card_loop_size)
    card_handshake: int = transform_subject(card_pubkey, door_loop_size)
    assert door_handshake == card_handshake
    assert door_handshake == 14897079
