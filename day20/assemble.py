import re
from contextlib import contextmanager
from typing import IO, ContextManager, Generator, List, Dict, Union, Tuple, DefaultDict, Optional
from math import isqrt, prod
from collections import defaultdict
from itertools import combinations


"""With the help of https://github.com/mebeim"""

@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def get_edges(tile: List[str], side: str) -> str:
    """
    This function extracts a specific side of a tile.
    """
    if side == "t":
        return tile[0]
    elif side == "b":
        return tile[-1]
    elif side == "l":
        return "".join([row[0] for row in tile])
    else:
        return "".join([row[-1] for row in tile])


def rotate90(tile: List[str]) -> List[str]:
    """
    This function rotates a tile 90 degrees clockwise.
    """
    rotated_tile: List[str] = list("".join(j for j in i) for i in zip(*tile[::-1]))
    return rotated_tile


def get_flip(tile: List[str]) -> List[str]:
    """
    This function flips a tile.
    """
    flipped_tile: List[str] = tile[::-1]
    return flipped_tile


def get_orientations(tile: List[str]) -> Generator[List[str], None, None]:
    """
    This generator function returns the possible rotations of a tile.
    """
    yield tile
    for _ in range(3):  # rotate 90, 180, 270
        tile = rotate90(tile)
        yield tile


def get_arrangements(tile: List[str]) -> Generator[List[str], None, None]:
    """
    This generator function returns the possible arragnements of a tile
    including rotations and flips.
    It calls onto the get_orientations generator function
    """
    yield from get_orientations(tile)
    flipped_tile: List[str] = get_flip(tile)
    yield from get_orientations(flipped_tile)
    # yield from get_orientations(tile[::-1])


def match_tiles(tiles: Dict[int, List[str]]) -> Dict[int, str]:
    """
    This function matches the tiles together and returns a
    dictionary containing the corner ids as the key 
    and the sides as the value.
    """
    matched_sides: DefaultDict[int, str] = defaultdict(str)
    # corners: Dict[int, str] = {}

    side_directions: List[str] = ["t", "b", "r", "l"]
    for tile1_id, tile2_id in combinations(tiles, 2):
        a: List[str] = tiles[tile1_id]
        b: List[str] = tiles[tile2_id]

        for a_side in side_directions:
            for b_side in side_directions:
                a_edge = get_edges(a, a_side)
                b_edge = get_edges(b, b_side)

                # do they match?
                if a_edge == b_edge or a_edge[::-1] == b_edge:
                    matched_sides[tile1_id] += a_side
                    matched_sides[tile2_id] += b_side

    corners: Dict[int, str] = {
        tile_id: sides for tile_id, sides in matched_sides.items() if len(sides) == 2
    }
    assert len(corners) == 4
    return corners


def find_match(
    tile: List[str],
    tiles: Dict[int, List[str]],
    matching_side_a: str,
    matching_side_b: str,
) -> Union[List[str], None]:
    """
    This function takes a specific tile, the dictionary of all the tiles,
    and two sides to match, e.g. 't' and 'b' and returns the tile
    whose 'b' side matches the first tile's 't' side.
    """
    original_side = get_edges(tile, matching_side_a)

    # iterate over every single tile from the tiles dictionary
    for other_tile_id, other_tile in tiles.items():
        # don't consider the same tile
        if tile is other_tile:
            continue

        # let's try arranging the other tile in all possible ways
        # until we find a match or not
        for other_variation in get_arrangements(other_tile):
            # if the two match
            if original_side == get_edges(other_variation, matching_side_b):
                tiles.pop(other_tile_id)
                return other_variation
    return None


def arrange_row(
    prev_tile: List[str], tiles: Dict[int, List[str]], per_row: int
) -> Generator[List[str], None, None]:
    """
    This function takes a starting tile, the dictionary of all the tiles
    and an integer number of tiles per_row and arranges a row.
    """
    yield prev_tile
    for _ in range(per_row - 1):
        next_tile: List[str] = find_match(prev_tile, tiles, "r", "l")
        prev_tile = next_tile
        yield prev_tile


def remove_tile_edges(tile: List[str]) -> List[str]:
    """
    This function removes the edges of a tile.
    """
    return [row[1:-1] for row in tile[1:-1]]


def build_puzzle(
    topleft_tile: List[str], tiles: Dict[int, List[str]], image_side_length: int
) -> List[List[str]]:
    """
    This function takes the starting tile in the topleft corner and builds the
    image using the functions already defined.
    """
    first_tile: List[str] = topleft_tile
    image: List[List[str]] = []

    while True:
        # build a row of tiles
        image_row: List[List[str]] = arrange_row(first_tile, tiles, image_side_length)
        # remove the edges from every single one of them
        image_row = map(remove_tile_edges, image_row)
        # add all of these tiles into a big row
        image.extend(map("".join, zip(*image_row)))

        # if no more tiles are left, stop
        if not tiles:
            break

        # once a row is built, find the first tile in the following row
        first_tile = find_match(first_tile, tiles, "b", "t")

    return image


def convert_pattern_to_indices(pattern: List[str]) -> List[Tuple[int, int]]:
    """
    This functions converts a pattern to indices indicating the '#' places.
    """
    indices: List[Tuple[int, int]] = []
    for row_index, row in enumerate(pattern):
        for col_index, col in enumerate(row):
            if col == "#":
                indices.append((row_index, col_index))
    return indices


def count_pattern_in_image(pattern: List[str], image: List[List[str]]) -> Optional[int]:
    """
    This function counts how many times a pattern appears in the image.
    """
    pattern_height: int = len(pattern)
    pattern_width: int = len(pattern[0])
    image_height: int = len(image)
    image_width: int = len(image[0])

    indices: List[Tuple[int, int]] = convert_pattern_to_indices(pattern)

    for image_arrangement in get_arrangements(image):
        found: int = 0
        for row in range(image_height - pattern_height):
            for col in range(image_width - pattern_width):
                if all(
                    image_arrangement[row + delta_row][col + delta_col] == "#"
                    for delta_row, delta_col in indices
                ):
                    found += 1

        if found != 0:
            return found
    return None


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    tiles: Dict[int, List[str]] = {}
    with cm as input_file:
        for block in input_file.read().split("\n\n"):
            tile = block.split("\n")
            tile_id: int = int(tile[0].split()[1][:-1])
            squares: List[str] = [j for j in tile[1:]]
            tiles[tile_id] = squares
    corners: List[int] = match_tiles(tiles)

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
    print("Part 2:", roughness)
