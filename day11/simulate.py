from collections import defaultdict
from contextlib import contextmanager
from typing import IO, ContextManager, DefaultDict, Dict, Generator, List, Tuple


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def swap_seats(seat_map: Dict[Tuple[int, int], str]) -> None:
    """
    This function swaps the seats based on the following rules:
    - if seat is empty ('L') and there are no occupied seats next to it,
    it becomes occupied
    - if occupied ('#') and 4 or more seats next to it are occupied,
    it becomes free
    - otherwise, no change
    - Floor slots ('.') never change
    When the layout does not change for two consecutive iterations, stop.
    """
    new_seat_map: Dict[Tuple[int, int], str] = {}
    n_occupied: int
    while True:
        for (row, col), seat in seat_map.items():
            if seat == ".":
                new_seat_map[row, col] = "."
            elif seat == "L":
                n_occupied = check_neighbours(seat_map, (row, col), "#")
                if n_occupied == 0:
                    new_seat_map[row, col] = "#"
            elif seat == "#":
                n_occupied = check_neighbours(seat_map, (row, col), "#")
                if n_occupied >= 4:
                    new_seat_map[row, col] = "L"
        if new_seat_map == seat_map:
            break
        for location, seat in new_seat_map.items():
            seat_map[location] = seat


def check_neighbours(
    seat_map: Dict[Tuple[int, int], str], pos: Tuple[int, int], interest: str
) -> int:
    """
    This functions checks the neighbourhood of a given position and returns the number
    of `interest` that there are.
    """
    row: int = pos[0]
    col: int = pos[1]
    neighbours: str = ""
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0) and (j == 0):
                continue
            neighbours += seat_map.get((row - i, col - j), ".")
    n_neighbours: int = neighbours.count(interest)
    return n_neighbours


def swap_diagonal_seats(seat_map: Dict[Tuple[int, int], str]) -> None:
    """
    This function swaps the seats based on the following rules:
    - it looks at each of the 8 possible directions but not just at the
    nearest seat (like in the `swap_seats` function)
    - if seat is empty ('L') and there are no visibly occupied seats,
    it becomes occupied
    - if occupied ('#') and 5 or more seats next to it are occupied,
    it becomes free
    - otherwise, no change
    - Floor slots ('.') never change
    When the layout does not change for two consecutive iterations, stop.
    """
    new_seat_map: Dict[Tuple[int, int], str] = {}
    n_occupied: int
    while True:
        for (row, col), seat in seat_map.items():
            if seat == ".":
                new_seat_map[row, col] = "."
            elif seat == "L":
                n_occupied = check_neighbourhood(seat_map, (row, col))
                if n_occupied == 0:
                    new_seat_map[row, col] = "#"
            elif seat == "#":
                n_occupied = check_neighbourhood(seat_map, (row, col))
                if n_occupied >= 5:
                    new_seat_map[row, col] = "L"
        if new_seat_map == seat_map:
            break
        for location, seat in new_seat_map.items():
            seat_map[location] = seat


def check_neighbourhood(
    seat_map: Dict[Tuple[int, int], str], pos: Tuple[int, int]
) -> int:
    """
    This functions checks the neighbourhood (including diagonal directions)
    and for every seat.
    """
    row: int = pos[0]
    col: int = pos[1]
    n_neighbours: int = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0) and (j == 0):
                continue
            n_neighbours += check_diagonal_directions(seat_map, row, col, (i, j))
    return n_neighbours


def check_diagonal_directions(
    seat_map: Dict[Tuple[int, int], str], row: int, col: int, direction: Tuple[int, int]
) -> int:
    """
    This function checks a specific direction for the first observed seat.
    """
    while True:
        row = row + direction[0]
        col = col + direction[1]
        try:
            if seat_map[row, col] == "#":
                return 1
            elif seat_map[row, col] == "L":
                return 0
        except KeyError:
            return 0


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    with cm as input_file:
        positions: List[List[str]] = [
            [position for position in line] for line in input_file.read().splitlines()
        ]
    pos_dict: Dict[Tuple[int, int], str] = {}
    for i, row in enumerate(positions):
        for j, seat in enumerate(row):
            pos_dict[i, j] = seat
    # make a copy of it to be used in part 2
    copy_pos_dict = {pos: seat for pos, seat in pos_dict.items()}
    # Part 1
    swap_seats(pos_dict)
    count: int = 0
    for seat in pos_dict.values():
        if seat == "#":
            count += 1
    print(count)
    # part 2

    swap_diagonal_seats(copy_pos_dict)
    count = 0
    for seat in copy_pos_dict.values():
        if seat == "#":
            count += 1
    print(count)
