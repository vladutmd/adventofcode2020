from contextlib import contextmanager
from math import prod
from operator import add
from typing import IO, ContextManager, Dict, Generator, List, Optional, Tuple


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()

if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    with cm as input_file:
        time: int = int(input_file.readline())
        
        buses: List[str] = [
            bus for bus in input_file.readline().split(',') 
        ]

    real_buses: List[int] = [
            int(bus) for bus in buses if bus != 'x'
        ]
    waiting: List[Tuple[int, int]] = [
        (i, i-time%i) for i in real_buses
    ]
    bus: Tuple[int, int] = min(waiting, key=lambda x: x[1])
    print(prod(bus))


    # part 2
    bus_offset: List[Tuple[int, int]] = [
        (offset, int(bus)) for offset, bus in enumerate(buses) if bus != 'x'
    ]
    timestep: int = 0
    product: int = 1
    for (offset, bus) in bus_offset:
        while ((timestep + offset) % bus != 0):
            timestep += product
        product *= bus
    print(timestep)