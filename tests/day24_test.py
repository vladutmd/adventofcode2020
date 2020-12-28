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
    Tuple,
)

import pytest

from ..day24.flip import file_read, get_tile_location, musical_tiles


@pytest.fixture
def tiles() -> DefaultDict[Tuple[int, int], bool]:
    """
    Returns the tiles.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day24")
    tiles: DefaultDict[Tuple[int, int], bool] = defaultdict(
        bool
    )  # where black = True = 1
    with cm as input_file:
        for line in input_file.read().splitlines():
            loc: Tuple[int, int] = get_tile_location(line)
            tiles[loc] = not tiles[loc]
    return tiles


def test_part1(tiles: DefaultDict[Tuple[int, int], bool]):
    """
    Tests if the tile dictionary was created correctly.
    """
    assert sum(tiles.values()) == 10


def test_musical_tiles(tiles: DefaultDict[Tuple[int, int], bool]):
    """
    Tests the `musical_tiles` function.
    """
    mus_tiles: DefaultDict[Tuple[int, int], bool] = tiles
    musical_tiles(mus_tiles)
    assert sum(mus_tiles.values()) == 2208