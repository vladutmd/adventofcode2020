import re
from collections import defaultdict, deque
from contextlib import contextmanager
from typing import IO, ContextManager, Deque, Dict, Generator, List, Tuple


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def line_processor(filename: str) -> Generator:
    """
    This generator takes a file line by line
    and processes one by one.
    """
    cm: ContextManager[IO] = file_read(filename)
    with cm as input_file:
        for line in input_file:
            if line.startswith("mask"):
                yield line.split("=")[1].strip()
            else:
                match = re.findall(r"mem\[(\d+)] = (\d+)", line)[0]
                yield (int(match[0]), int(match[1]))


def apply_bitmask(mask: str, value: int) -> int:
    """
    This functions applies the bitmask to a specific value
    and returns the new integer.
    """
    binary_list: List[str] = [bit for bit in f"{value:036b}"]
    for index, character in enumerate(mask):
        if character.isdigit():
            binary_list[index] = character
    return int("".join(binary_list), 2)


def apply_floatmask(mask: str, address: int) -> List[int]:
    """
    This function applies the floatmask to the original memory
    address and returns all possible float variations.
    """
    binary_list: List[str] = [bit for bit in f"{address:036b}"]
    addresses: Deque[str] = deque()
    for index, character in enumerate(mask):
        if character == "0":
            continue
        binary_list[index] = character
    binary_string: str = "".join(x for x in binary_list)
    addresses.append(binary_string)
    while "X" in addresses[0]:
        working_string: str = addresses.popleft()
        for i in range(2):
            addresses.append(working_string.replace("X", str(i), 1))
    return [int(i, 2) for i in addresses]


if __name__ == "__main__":
    memory_dict: Dict[int, int] = {}
    for instruction in line_processor("input"):
        if isinstance(instruction, str):
            mask: str = instruction
        else:
            address: int = instruction[0]
            value: int = instruction[1]
            memory_dict[address] = apply_bitmask(mask, value)
    print(sum(memory_dict.values()))

    new_memory_dict: Dict[int, int] = {}
    for instruction in line_processor("input"):
        if isinstance(instruction, str):
            new_mask: str = instruction
        else:
            new_address: int = instruction[0]
            new_value: int = instruction[1]
            new_addresses = apply_floatmask(new_mask, new_address)
            for new_address in new_addresses:
                new_memory_dict[new_address] = new_value
    print(sum(new_memory_dict.values()))
