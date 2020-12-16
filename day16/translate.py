import re
from collections import defaultdict, deque
from contextlib import contextmanager
from itertools import chain
from typing import (IO, ContextManager, Dict, Generator, List, Set, Tuple,
                    ValuesView)


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
            if "or" in line:  # it#s a r
                words: List[str] = re.findall(r"([a-z]+)+", line)
                number_ranges_str: List[str] = re.findall(r"[(\d+)\-(\d+)]+", line)
                number_ranges: List[Tuple[int, ...]] = [
                    tuple(
                        int(num) + 1
                        if number_range.split("-").index(num) == 1
                        else int(num)
                        for num in number_range.split("-")
                    )
                    for number_range in number_ranges_str
                ]
                key: str = " ".join(words[:-1])
                yield {key: number_ranges}
            else:
                numbers_str: List[str] = line.split(",")
                if len(numbers_str) > 1:
                    yield [int(num) for num in numbers_str]


def validate_ticket(ticket: List[int], ranges: List[Tuple[int, int]]) -> int:
    """
    This functions takes a `ticket` as a list of integers,
    and a a list of valid ranges
    and checks if all the numbers are in ANY of the valid ranges.
    Returns an int, the ticket number that is not in any range or 0
    """
    for number in ticket:
        if not any(
            number in range(*num_range) for num_range in chain.from_iterable(ranges)
        ):
            return number
    return 0


def validate_tickets(
    tickets: List[List[int]], rules_dict: Dict[str, List[Tuple[int, int]]]
) -> List[List[int]]:
    """
    This function only returns the valid tickets.
    """
    invalid_ticket_indices: List[int] = []
    for index, ticket in enumerate(tickets):
        if validate_ticket(ticket, rules_dict.values()):
            invalid_ticket_indices.append(index)
    valid_tickets: List[List[int]] = [
        ticket
        for (index, ticket) in enumerate(tickets)
        if index not in invalid_ticket_indices
    ]
    return valid_tickets


def determine_field_orders(
    tickets: List[List[int]], rules_dict: Dict[str, List[Tuple[int, int]]]
) -> Dict[str, int]:
    """
    This functions takes a list of valid tickets, the rules_dict and
    returns a dictionary with the field as the key and its position as the
    value.
    """
    field_possibilities: Dict[int, set] = {}
    # go through each set of numbers from each position in all the
    # valid tickets
    for field_pos, number_at_pos in enumerate(zip(*tickets)):
        s = set()
        for option_pos, option in enumerate(rules_dict.values()):
            if all(
                any(number in range(*num_range) for num_range in option)
                for number in number_at_pos
            ):
                s.add(option_pos)
        field_possibilities[field_pos] = s
    # ok so the problem with my original code was that there might be
    # multiple candidates for each position
    # so let's start with the field that only has one candidate
    # find the shortest set, don't change it
    # remove that value from all other sets
    # repeat until each set is 1 element long
    order_dict: Dict[int, int] = {}
    while sum(len(sets) for sets in field_possibilities.values()) != len(
        field_possibilities.values()
    ):
        # find the shortest set
        pos: int = min(field_possibilities, key=lambda x: len(field_possibilities[x]))
        value: Set[int] = field_possibilities[pos]
        for key, values in field_possibilities.items():
            if key != pos:
                field_possibilities[key] = values - value
        order_dict.update({pos: value.pop()})
        del field_possibilities[pos]
    order_dict.update({key: value.pop() for key, value in field_possibilities.items()})
    map_dict: Dict[str, int] = {}
    for location, key in enumerate(rules_dict.keys()):
        for pos_key, pos_value in order_dict.items():
            if location == pos_value:
                map_dict[key] = pos_key
    return map_dict


if __name__ == "__main__":
    rules_dict: Dict[str, List[Tuple[int, int]]] = {}
    tickets: List[List[int]] = []
    for line in line_processor("input"):
        if isinstance(line, dict):
            rules_dict.update(line)
        else:
            tickets.append(line)
    sum_num: int = 0
    my_ticket: List[int] = tickets.pop(0)
    # now tickets refers to other tickets
    for ticket in tickets:
        sum_num += validate_ticket(ticket, rules_dict.values())
    print(sum_num)

    # part 2
    valid_tickets = validate_tickets(tickets, rules_dict)
    map_dict = determine_field_orders(valid_tickets, rules_dict)
    product: int = 1
    for key, value in map_dict.items():
        if key.startswith("departure"):
            product *= my_ticket[value]
    print(product)
