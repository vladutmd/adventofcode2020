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


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def get_tile_location(dir_string: str) -> Tuple[int, int]:
    """
    This function reads in a string such as sesenwnenenewseeswwswswwnenewsewsw
    and returns the location of the tile from a starting point 0,0.
    """
    mapping: Dict[str, str] = {
        "ne": "0,1,",
        "nw": "-1,1,",
        "se": "1,-1,",
        "sw": "0,-1,",
        "e": "1,0,",
        "w": "-1,0,",
    }
    x: int = 0
    y: int = 0
    # substitute ne, nw, se, etc. with the corresponding numbers
    for letters, numbers in mapping.items():
        dir_string = dir_string.replace(letters, numbers)
    directions = [int(i) for i in dir_string.split(",") if i != ""]
    # x,y,x,y,x,y,x,y,x,y,x,y etc
    for dx, dy in zip(directions[0::2], directions[1::2]):
        x += dx
        y += dy
    return (x, y)


def musical_tiles(tiles: DefaultDict[Tuple[int, int], bool], n_days: int = 100) -> None:
    """
    This functions plays musical tiles.
    Every day tiles are flipped according to the following rules:
        - any black tile with 0 or more than 2 black tiles immediately
        adjacent to it is flipped to white
        - any white tile with exactly 2 black times immediately adjacent
        to it is flipped to black
    Adjacent tiles refer to the 6 neighbours of each tile.
    The rules are applied simultaneously:
    i.e. record the changes and then apply the changes all at once
    """
    mapping: List[Tuple[int, int]] = [
        (0, 1),
        (-1, 1),
        (1, -1),
        (0, -1),
        (1, 0),
        (-1, 0),
    ]

    for _ in range(n_days):
        # create a dictionary to store the number of adjacent black tiles
        # at each location
        neighbour_count: DefaultDict[Tuple[int, int], int] = defaultdict(int)
        for position in tiles.keys():
            neighbour_count[position] = 0
        # set the neighbouring count of all position to 0
        # but isn't it a defaultdict? why do we have to do that?
        # because in the last part, when we iterate over neighbour_count.items()
        # unless we "accessed" these already, they wouldn't show up
        for (x, y), is_black in tiles.items():  # iterate over all the tiles
            if is_black:  # if it is 1, i.e. black
                for dx, dy in mapping:  # increment the neighbours' count
                    neighbour_count[x + dx, y + dy] += 1
        for position, count in neighbour_count.items():
            if tiles[position]:  # i.e. if it is black
                if count == 0 or count > 2:
                    tiles[position] = False
            else:  # i.e. if it is white
                if count == 2:
                    tiles[position] = True


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    tiles: DefaultDict[Tuple[int, int], bool] = defaultdict(
        bool
    )  # where black = True = 1
    with cm as input_file:
        for line in input_file.read().splitlines():
            loc: Tuple[int, int] = get_tile_location(line)
            tiles[loc] = not tiles[loc]
    # part 1
    print(sum(tiles.values()))
    # part 2
    musical_tiles(tiles)
    print(sum(tiles.values()))
