from collections import defaultdict
from contextlib import contextmanager
from typing import (IO, ContextManager, DefaultDict, Dict, Generator, List,
                    Tuple)


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def evolve_state(space_map: Dict[Tuple[int, int, int], str], cycles: int) -> None:
    """
    Evolve the state of the pocket dimesion. The rules are such:
    - each cube at a specific position only ever considers its neighbours
    (i wonder if in part 2 all of a sudden that "ever" will be a lie haha)
    - cubes start either active '#' or inactive '.'
    - check 26 neighbours and SIMULTANEOUSLY change state
    (i.e. update values on a copy haha, don't make same mistake as in day 11)
    - if a cube is active and 2 or 3 of its neighbours are active, remain active
    - otherwise, becomes inactive (# to .)
    - if inactive '.' but 3 of its neighbours are active, becomes active '#'
    - otherwise stays inactive
    """
    new_space_map: DefaultDict[Tuple[int, int, int], str] = defaultdict(lambda: ".")
    for _ in range(cycles):
        # first iterate through each of the neighbours once. why?
        # so that the layers on either side are also created
        for (row, col, depth) in space_map.copy():
            create_neighbours(space_map, (row, col, depth))

        # so let's iterate through those values
        # for (row, col, depth), cube in space_map.items():

        for (row, col, depth) in space_map.copy():
            cube = space_map[row, col, depth]
            if cube == "#":
                n_occupied = check_neighbours(space_map, (row, col, depth), "#")
                if 2 <= n_occupied <= 3:
                    continue
                else:
                    new_space_map[row, col, depth] = "."
            elif cube == ".":
                n_occupied = check_neighbours(space_map, (row, col, depth), "#")
                if n_occupied == 3:
                    new_space_map[row, col, depth] = "#"
                else:
                    continue
        for location, cube in new_space_map.items():
            space_map[location] = cube


def create_neighbours(
    space_map: Dict[Tuple[int, int, int], str], pos: Tuple[int, int, int]
) -> None:
    """
    Checks the existence of a position thus creating it. Nothing else.
    """
    row: int = pos[0]
    col: int = pos[1]
    depth: int = pos[2]
    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                space_map[(row - i, col - j, depth - k)]


def check_neighbours(
    space_map: Dict[Tuple[int, int, int], str], pos: Tuple[int, int, int], interest: str
) -> int:
    """
    This functions checks the neighbourhood of a given position and returns the number
    of `interest` that there are.
    """
    row: int = pos[0]
    col: int = pos[1]
    depth: int = pos[2]
    neighbours: str = ""
    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                if (i == 0) and (j == 0) and (k == 0):
                    continue
                neighbours += space_map[(row - i, col - j, depth - k)]
    n_neighbours: int = neighbours.count(interest)
    return n_neighbours


def evolve_hyperstate(
    hyper_space_map: Dict[Tuple[int, int, int, int], str], cycles: int
) -> None:
    """
    Evolve the state of the pocket dimesion. The rules are such:
    - each cube at a specific position only ever considers its neighbours
    (i wonder if in part 2 all of a sudden that "ever" will be a lie haha)
    - cubes start either active '#' or inactive '.'
    - check 26 neighbours and SIMULTANEOUSLY change state
    (i.e. update values on a copy haha, don't make same mistake as in day 11)
    - if a cube is active and 2 or 3 of its neighbours are active, remain active
    - otherwise, becomes inactive (# to .)
    - if inactive '.' but 3 of its neighbours are active, becomes active '#'
    - otherwise stays inactive
    """
    new_hyper_space_map: DefaultDict[Tuple[int, int, int, int], str] = defaultdict(
        lambda: "."
    )
    for cycle in range(cycles):

        for (row, col, depth, hyper) in hyper_space_map.copy().keys():
            create_hyperneighbours(hyper_space_map, (row, col, depth, hyper))

        for (row, col, depth, hyper) in hyper_space_map.copy():
            cube = hyper_space_map[row, col, depth, hyper]
            if cube == "#":
                n_occupied = check_hyperneighbours(
                    hyper_space_map, (row, col, depth, hyper), "#"
                )
                if 2 <= n_occupied <= 3:
                    continue
                else:
                    new_hyper_space_map[row, col, depth, hyper] = "."
            elif cube == ".":
                n_occupied = check_hyperneighbours(
                    hyper_space_map, (row, col, depth, hyper), "#"
                )
                if n_occupied == 3:
                    new_hyper_space_map[row, col, depth, hyper] = "#"
                else:
                    continue
        for location, cube in new_hyper_space_map.items():
            hyper_space_map[location] = cube


def create_hyperneighbours(
    hyper_space_map: Dict[Tuple[int, int, int, int], str],
    pos: Tuple[int, int, int, int],
) -> None:
    """
    Checks the existence of a position thus creating it. Nothing else.
    """
    row: int = pos[0]
    col: int = pos[1]
    depth: int = pos[2]
    hyper: int = pos[3]
    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                for l in range(-1, 2):
                    hyper_space_map[(row - i, col - j, depth - k, hyper - l)]


def check_hyperneighbours(
    hyper_space_map: Dict[Tuple[int, int, int, int], str],
    pos: Tuple[int, int, int, int],
    interest: str,
) -> int:
    """
    This functions checks the neighbourhood of a given position and returns the number
    of `interest` that there are.
    """
    row: int = pos[0]
    col: int = pos[1]
    depth: int = pos[2]
    hyper: int = pos[3]
    neighbours: str = ""
    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if (i == 0) and (j == 0) and (k == 0) and (l == 0):
                        continue
                    neighbours += hyper_space_map[
                        (row - i, col - j, depth - k, hyper - l)
                    ]
    n_neighbours: int = neighbours.count(interest)
    return n_neighbours


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    with cm as input_file:
        positions: List[List[str]] = [
            [position for position in line] for line in input_file.read().splitlines()
        ]
    # Part 1
    space_map: DefaultDict[Tuple[int, int, int], str] = defaultdict(lambda: ".")
    for i, row in enumerate(positions):
        for j, cube in enumerate(row):
            space_map[i, j, 0] = cube
    evolve_state(space_map, 6)
    count: int = 0
    for cube in space_map.values():
        if cube == "#":
            count += 1
    print(count)

    # Part 2
    hyper_space_map: DefaultDict[Tuple[int, int, int, int], str] = defaultdict(
        lambda: "."
    )
    for i, row in enumerate(positions):
        for j, cube in enumerate(row):
            hyper_space_map[i, j, 0, 0] = cube
    evolve_hyperstate(hyper_space_map, 6)
    count = 0
    for cube in hyper_space_map.values():
        if cube == "#":
            count += 1
    print(count)
