from math import prod
from timeit import timeit
from typing import List, Dict, ContextManager, Generator, IO
from contextlib import contextmanager

@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()

def find_sum_two(numbers_list: List[int], n: int) -> List[int]:
    """
    Finds two numbers that add up to n
    or returns False.
    :numbers_list: a list of numbers
    :n: the sum required
    """

    # using a dictionary rather than brute force
    found: Dict[int, int] = {}
    for number in numbers_list:
        try:
            found[n-number]
            return [n-number, number]
        except:
            found[number] = 0
    return []


def find_sum_three(numbers_list: List, n: int) -> List[int]:
    """
    Finds three numbers that add up to n
    or returns False.
    :numbers_list: a list of numbers
    :n: the sum required
    """

    # for each element, check if there are two other elements that give
    # a sum of n-element
    for number in numbers_list:
        # check if there are two numbers that give you the sum
        two_numbers = find_sum_two([x for x in numbers_list if x != number], n-number)
        if two_numbers:
            return [number, *two_numbers]
    return []

if __name__ == '__main__':
    cm: ContextManager[IO] = file_read('input')
    with cm as input_file:
        data: str = input_file.read()
    numbers: List[int] = [int(i) for i in data.split()]
    print(prod(find_sum_two(numbers, 2020)))
    print(prod(find_sum_three(numbers, 2020)))
