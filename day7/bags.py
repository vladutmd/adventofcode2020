import re
from collections import defaultdict, deque
from contextlib import contextmanager
from typing import (IO, ContextManager, DefaultDict, Deque, Generator, List,
                    Set, Tuple, Optional, Match)


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def process_rules(
    rules: List[str],
) -> Tuple[DefaultDict[str, List[Tuple[int, str]]], DefaultDict[str, Set[str]]]:
    """
    This function goes through each of the elements and processes them,
    storing them in a suitable format. What is that?
    """
    has: DefaultDict[str, List[Tuple[int, str]]] = defaultdict(list)
    isin: DefaultDict[str, Set[str]] = defaultdict(set)
    for rule in rules:
        owner = re.match(r"(\w+ \w+)", rule)[0]
        workers: List[Tuple[str, str]] = re.findall(r"(\d+) (\w+ \w+)", rule)
        # now let's store them in our `has` and `isin` structures
        for number, worker in workers:
            has[owner].append((int(number), worker))
            isin[worker].add(owner)
    return (has, isin)


def how_many_colours_contain(
    has_list: DefaultDict[str, List[Tuple[int, str]]],
    isin_list: DefaultDict[str, Set[str]],
    colour: str,
) -> int:
    """
    This functions returns the number of bag
    colours that contain a specific colour.
    """
    bags_containing_colour: Set[str] = set()
    # create a double ended queue
    # we start with only having shiny gold in it
    color_deque: Deque[str] = deque([colour])
    # while the deque still has colour left to process
    # the following code runs
    while color_deque:
        # pop the color that was first put in (i.e. first shiny gold, then the colors)
        # containing it
        # and so on until nothng else
        col: str = color_deque.popleft()
        # now check which colour bags contain the correct colour
        # and iterate over them
        for containing_colour in isin[col]:
            # if we haven't already seen this colour before, add it to our set
            # and append the current colour to the deque so that we check its parents later
            if containing_colour not in bags_containing_colour:
                bags_containing_colour.add(containing_colour)
                color_deque.append(containing_colour)
    # if we have looked at all the direct parents, grandparents, grandgrandparents, and all
    # the way to our ancestors, let's return how many people are in our family tree
    return len(bags_containing_colour)


def how_many_bags(
    has_list: DefaultDict[str, List[Tuple[int, str]]], colour: str
) -> int:
    """
    This function counts how many bags a single colour bag
    must contain.
    """
    bag_collection: int = 0
    # iterate over the list of bags that a "colour" bag contains
    for bag in has_list[colour]:
        # for each colour, add its count as well as the count multiplied
        # by each of its coloured children bags. it's recursive
        bag_collection += bag[0] * (1 + how_many_bags(has_list, bag[1]))
    return bag_collection


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    with cm as input_file:
        rules: List[str] = input_file.read().splitlines()
    has, isin = process_rules(rules)
    print(how_many_colours_contain(has, isin, "shiny gold"))
    print(how_many_bags(has, "shiny gold"))