from contextlib import contextmanager
from math import prod
from typing import IO, ContextManager, Dict, Generator, List, Tuple


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def find_earliest_bus(time: int, buses: List[int]) -> Tuple[int, int]:
    """
    This function returns the first bus one can take.
    """
    waiting: List[Tuple[int, int]] = [(i, i - time % i) for i in buses]
    bus: Tuple[int, int] = min(waiting, key=lambda x: x[1])
    return bus


def find_first_timestamp_matching_offsets(
    bus_with_offsets: List[Tuple[int, int]]
) -> int:
    """
    Uses the Chinese remainder theorem to find the first timestep where
    all the offset timestamps match.
    """
    timestep: int = 0
    product: int = 1
    for (offset, bus) in bus_with_offsets:
        while (timestep + offset) % bus != 0:
            timestep += product
        product *= bus
    return timestep


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    with cm as input_file:
        time: int = int(input_file.readline())

        buses: List[str] = [bus for bus in input_file.readline().split(",")]
    real_buses: List[int] = [int(bus) for bus in buses if bus != "x"]
    print(prod(find_earliest_bus(time, real_buses)))

    # part 2
    bus_offset: List[Tuple[int, int]] = [
        (offset, int(bus)) for offset, bus in enumerate(buses) if bus != "x"
    ]
    print(find_first_timestamp_matching_offsets(bus_offset))
