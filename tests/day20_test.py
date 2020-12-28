import os
import re
from collections import defaultdict
from contextlib import contextmanager
from itertools import combinations
from math import isqrt, prod
from typing import (
    IO,
    ContextManager,
    DefaultDict,
    Dict,
    Generator,
    List,
    Optional,
    Tuple,
    Union,
)

import pytest

from ..day20.assemble import (
    arrange_row,
    build_puzzle,
    convert_pattern_to_indices,
    count_pattern_in_image,
    file_read,
    find_match,
    get_arrangements,
    get_edges,
    get_flip,
    get_orientations,
    match_tiles,
    remove_tile_edges,
    rotate90,
)


@pytest.fixture
def tiles() -> Dict[int, List[str]]:
    """
    Returns the test set of tiles.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day20")
    tiles: Dict[int, List[str]] = {}
    with cm as input_file:
        for block in input_file.read().split("\n\n"):
            tile = block.split("\n")
            tile_id: int = int(tile[0].split()[1][:-1])
            squares: List[str] = [j for j in tile[1:]]
            tiles[tile_id] = squares
    return tiles


def test_part1_corners(tiles: Dict[int, List[str]]):
    """
    Tests the `match_tiles` function that returns the corners.
    """
    corners: Dict[int, List[str]] = match_tiles(tiles)
    assert prod(corners) == 20899048083289


def test_part2_monsters(tiles: Dict[int, List[str]]):
    """
    Tests the count monsters in part 2 and all other functions that are needed
    for it.
    """
    corners: Dict[int, List[str]] = match_tiles(tiles)
    # ok let's get a corner and start building the image
    topleft_id: int
    topleft_sides: str
    topleft_id, matching_sides = corners.popitem()
    # get the corresponding topleft tile
    topleft_tile: List[str] = tiles[topleft_id]
    # let's rotate it so that the matched sides are to the right ('r')
    # and bottom 'b'``
    if matching_sides in ["tr", "rt"]:
        topleft_tile = rotate90(topleft_tile)
    elif matching_sides in ["tl", "lt"]:
        for _ in range(2):
            topleft_tile = rotate90(topleft_tile)
    elif matching_sides in ["bl", "lb"]:
        for _ in range(3):
            topleft_tile = rotate90(topleft_tile)

    # what is the shape of our image?
    image_side_length = isqrt(len(tiles))

    # remove the topleft tile since we have rotated it
    tiles.pop(topleft_id)
    image = build_puzzle(topleft_tile, tiles, image_side_length)

    # in order to find the monsters, we need to find all variations of it
    # in all of the image variations
    monster_pattern = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ]
    number_monsters: int = count_pattern_in_image(monster_pattern, image)
    # now the roughness is defined as the number of '#'s that are not
    # part of a monster
    total_hashes: int = sum(row.count("#") for row in image)
    hashes_per_monster: int = sum(row.count("#") for row in monster_pattern)
    total_monster_hashes: int = number_monsters * hashes_per_monster
    roughness: int = total_hashes - total_monster_hashes
    assert roughness == 273
