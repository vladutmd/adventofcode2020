from contextlib import contextmanager
from math import prod
from typing import IO, ContextManager, Generator, List, Tuple


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def slide_down(topology: List[List[int]], slope: Tuple[int, int]) -> int:
    """
    This function takes a local topology map and a slope of travel.
    Then it goes down the map at the correct slope taking into
    account periodic boundary conditions in the column direction
    until it goes past the lowest row of the map.
    It takes three arguments:
        :topology: a 2D array of 1s and 0s where the 1s represent trees
        :slope: a tuple of two integers representing the right and down
        components.
    It returns an integer corresponding to the number of trees encountered
    along the way.
    """
    right: int = slope[0]
    down: int = slope[1]
    row: int = 0
    col: int = 0
    trees: int = 0
    width = len(topology[0])
    while True:
        try:
            trees += topology[row][col % width]
            row += down
            col += right
        except IndexError:
            return trees


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    with cm as input_file:
        input_map: List[str] = input_file.read().splitlines()
    processed_map: List[List[int]] = [
        [0 if i == "." else 1 for i in j] for j in input_map
    ]
    slopes: List[Tuple[int, int]] = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    print(slide_down(processed_map, (3, 1)))
    print(prod([slide_down(processed_map, i) for i in slopes]))
