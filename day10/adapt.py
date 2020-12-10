from contextlib import contextmanager
from operator import mul, sub
from typing import IO, ContextManager, Dict, Generator, List


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def calculate_differences(adapters: List[int]) -> List[int]:
    """
    Calculates the differences between successive elements in a list.
    """
    differences: List[int] = list(map(sub, adapters[1:], adapters[:-1]))
    return differences


def count_differences(differences: List[int]) -> Dict[int, int]:
    """
    This functions counts how many 1s there are and how many 3s there are
    and returns a dictionary.
    """
    counts: Dict[int, int] = {1: differences.count(1), 3: differences.count(3)}
    return counts


def count_difference_patterns(differences: List[int]) -> Dict[int, int]:
    """
    This function counts how many variations of consecutive differences there are.
    For example, 1 1, or 1 1 1 or 1 1 1 1 or that's it.
    So need to count how many of those are in there and return a dictionary.
    Is there a way to count a sublist in a list?
    maybe, but i'll convert to a string :D
    """
    difference_string: str = "".join(str(difference) for difference in differences)
    counts: Dict[int, int] = {}
    for pattern in ["1111", "111", "11"]:
        counts.update({len(pattern): difference_string.count(pattern)})
        difference_string = difference_string.replace(pattern, "")
    return counts


def calculate_arrangements(arrangements_dict: Dict[int, int]) -> int:
    """
    From a count dictionary of permutations, count how many ways there
    are of arranging the adapters.
    If there are two 1s in a row, there are two permutations: 1 1 or a difference of 2.
    If there are three 1s in a row, there are 4 permutations: 1 1 1, 2 1, 1 2, 3
    If there are four 1s in a row, there are 7 permutations: 1 1 1 1, 2 1 1, 1 2 1, 1 1 2,
    2 2, 3 1, 1 3
    """
    arrangements: int = 1
    perm_dict: Dict[int, int] = {2: 2, 3: 4, 4: 7}
    for perm, occur in arrangements_dict.items():
        arrangements = (perm_dict[perm] ** occur) * arrangements
    return arrangements


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    with cm as input_file:
        adapters: List[int] = [int(line) for line in input_file.read().splitlines()]
    adapters.append(0)
    adapters.append(max(adapters) + 3)
    adapters.sort()
    differences: List[int] = calculate_differences(adapters)
    # Part 1
    counts: Dict[int, int] = count_differences(differences)
    print(mul(*counts.values()))
    # Part 2
    pair_counts: Dict[int, int] = count_difference_patterns(differences)
    adapter_arrangements: int = calculate_arrangements(pair_counts)
    print(adapter_arrangements)
