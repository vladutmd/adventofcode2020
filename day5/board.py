from contextlib import contextmanager
from typing import IO, ContextManager, Generator, List, Set


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def decode_pass(boarding_pass: str) -> int:
    """
    This function takes a string such as 'FBFBBFFRLR'
    and performs some binary search in an array of integers
    0 to 127.
    """
    # the first seven characters refer to the rows
    row = int(boarding_pass[:7].replace("F", "0").replace("B", "1"), 2)
    # the last three characters refer to the columns
    col = int(boarding_pass[-3:].replace("L", "0").replace("R", "1"), 2)
    seat_id: int = row * 8 + col
    return seat_id


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    with cm as input_file:
        passes: List[str] = input_file.read().splitlines()
    max_pass: int = 0
    seat_ids: Set[int] = set()
    for boarding_pass in passes:
        current_id: int = decode_pass(boarding_pass)
        seat_ids.add(current_id)
        if current_id > max_pass:
            max_pass = current_id
    print(max_pass)
    low: int = min(seat_ids)
    high: int = max(seat_ids) + 1
    print((set([x for x in range(low, high)]) - seat_ids).pop())
