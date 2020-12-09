from typing import Dict, List


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
            found[n - number]
            return [n - number, number]
        except:
            found[number] = 0
    return []
