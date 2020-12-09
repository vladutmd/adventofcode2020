from collections import deque
from contextlib import contextmanager
from typing import IO, ContextManager, Deque, Generator, List

from .search import find_sum_two


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def process_list(numbers: List[int], n: int) -> int:
    """
    This function returns the first number in the list (after the preamble)
    which is not a sum of two of the X numbers before it.
    Uses the search function from day1
    """
    d: Deque[int] = deque(numbers[:n], maxlen=n)
    for number in numbers[n:]:
        if len(find_sum_two(list(d), number)) == 2:
            d.append(number)
        else:
            return number
    return -1


def break_encryption(numbers: List[int], n: int) -> int:
    """
    This function returns the sum of the smallest and largest
    number in a contiguous set of at least two numbers from the
    list that sum up to the number `n`.
    """
    # first try 2, then 3, then 4, and so on
    for i in range(2, len(numbers)):
        d: Deque[int] = deque(numbers[:i], maxlen=i)
        for j in numbers[i:]:
            if sum(d) == n:
                return min(d) + max(d)
            else:
                d.append(j)
    return -1


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    with cm as input_file:
        numbers: List[int] = [int(line) for line in input_file.read().splitlines()]
    # print(numbers)
    ans: int = process_list(numbers, 25)
    print(ans)
    index: int = numbers.index(ans)
    # only send it the part of the list until that number
    print(break_encryption(numbers[:index], ans))
