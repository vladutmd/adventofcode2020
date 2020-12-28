import os
from collections import defaultdict, deque
from contextlib import contextmanager
from itertools import islice
from typing import (
    IO,
    ContextManager,
    DefaultDict,
    Deque,
    Dict,
    Generator,
    List,
    Set,
    Tuple,
)

import pytest

from ..day22.cards import file_read, play_easy_game, play_recursive_combat


@pytest.fixture
def cards_input() -> Tuple[Deque[int], Deque[int]]:
    """
    Returns player 1 and player 2 cards.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day22")
    p1_cards: Deque[int] = deque()
    p2_cards: Deque[int] = deque()

    with cm as input_file:
        p1: str
        p2: str
        p1, p2 = [block for block in input_file.read().split("\n\n")]

    for card in p1.split("\n")[::-1]:
        if card.isdigit():
            p1_cards.append(int(card))
    for card in p2.split("\n")[::-1]:
        if card.isdigit():
            p2_cards.append(int(card))
    return (p1_cards, p2_cards)


def test_easy_game(cards_input: Tuple[Deque[int], Deque[int]]):
    """
    Tests the `play_easy_game` function.
    """
    winning_stack: Deque[int] = play_easy_game(*cards_input)
    assert sum((index + 1) * card for index, card in enumerate(winning_stack)) == 306


def test_recursive_combat(cards_input: Tuple[Deque[int], Deque[int]]):
    """
    Tests the `play_recursive_combat` function.
    """
    p1_cards_part2: Deque[int]
    p2_cards_part2: Deque[int]
    p1_cards_part2, p2_cards_part2 = cards_input
    winner, _ = play_recursive_combat(p1_cards_part2, p2_cards_part2, set())
    assert winner == 2
    assert sum((index + 1) * card for index, card in enumerate(p2_cards_part2)) == 291
