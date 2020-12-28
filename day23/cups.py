from collections import deque
from time import time
from typing import Deque, Dict, Generator, List, Set, Tuple


def play_cups(arrangement: Deque[int]) -> str:
    """
    This function plays cups.
    """
    current_cup: int = 0
    destination_cup: int
    for _ in range(100):
        if current_cup == 0:
            current_cup = arrangement[0]
        current_cup_index: int = arrangement.index(current_cup)
        removed_cups_indices: List[int] = [
            (current_cup_index + i) % len(arrangement) for i in range(1, 4)
        ]
        # not removing by index because after each pop the index will be different
        # let's get their values and remove by value
        removed_cups: List[int] = [arrangement[index] for index in removed_cups_indices]
        # now remove those values
        for value in removed_cups:
            arrangement.remove(value)
        destination_cup = current_cup - 1
        if destination_cup in removed_cups:
            while destination_cup in removed_cups:
                destination_cup -= 1
        if destination_cup < min(arrangement):
            destination_cup = max(arrangement)
        # ok now we have a destinaton cup
        # let's place the removed cups after it
        destination_cup_index: int = arrangement.index(destination_cup)
        while removed_cups != []:
            arrangement.insert(destination_cup_index + 1, removed_cups.pop())
        current_cup_index = (arrangement.index(current_cup) + 1) % len(arrangement)
        current_cup = arrangement[current_cup_index]
    final: str = ""
    index_1: int = arrangement.index(1)
    for i in range(1, 9):
        final += str(arrangement[(index_1 + i) % len(arrangement)])
    return final


def part1_with_dict(inputstring: str) -> str:

    cups = [int(num) for num in inputstring]
    cup_dictionary: Dict[int, int] = {}
    """
    Now we will store the cups in a dictionary
    where the key is the cup's value
    and the value is the following cup's value.
    Linked list using dictionary instead of using a LinkedList class
    and a Node class
    """
    for i in range(len(cups) - 1):
        cup_dictionary[cups[i]] = cups[i + 1]
    # for the last cup as a key, manually set its value to point to
    # the first element
    cup_dictionary[cups[-1]] = cups[0]

    current_cup: int = 0
    destination_cup: int
    cup1: int
    cup2: int
    cup3: int
    for _ in range(100):
        if current_cup == 0:
            current_cup = cups[0]

        cup1 = cup_dictionary[current_cup]
        cup2 = cup_dictionary[cup1]
        cup3 = cup_dictionary[cup2]

        three_cups = [cup1, cup2, cup3]
        # to "remove" the three elements, make the current_cup
        # point to the cup after cup3 in the dictionary
        cup_dictionary[current_cup] = cup_dictionary[cup3]

        # get the destination cup
        destination_cup = current_cup - 1
        # now the value of the destination_cup can either by in the three_cups
        # if so, keep subtracting 1 until it finds a cup that wasn't picked up
        while destination_cup in three_cups:
            destination_cup -= 1
        if destination_cup < min(cup_dictionary):
            destination_cup = max(
                num for num in cup_dictionary if num not in three_cups
            )

        # make cup 3 point where the destination cup was originally pointing
        cup_dictionary[cup3] = cup_dictionary[destination_cup]
        # make the destination cup point to cup1 now
        cup_dictionary[destination_cup] = cup1
        # cup 1 still points to cup2
        # cup 2 still points to cup 3

        # get the new current cup which is the next one
        current_cup = cup_dictionary[current_cup]

        # let's print the current order
        # we want the one after 1
    cup_we_want = cup_dictionary[1]
    l = []
    l.append(cup_we_want)
    for i in range(7):
        cup_we_want = cup_dictionary[cup_we_want]
        l.append(cup_we_want)
    final: str = "".join(str(i) for i in l)
    return final


def long_game_of_cups(inputstring: str) -> str:

    cups = [int(num) for num in inputstring]
    cup_dictionary: Dict[int, int] = {}
    """
    Now we will store the cups in a dictionary
    where the key is the cup's value
    and the value is the following cup's value.
    Linked list using dictionary instead of using a LinkedList class
    and a Node class
    """

    for i in range(len(cups) - 1):
        cup_dictionary[cups[i]] = cups[i + 1]
    cup_dictionary[cups[-1]] = max(cups) + 1

    for i in range(len(cups), 1000000):
        cup_dictionary[i + 1] = i + 2
    # for the last cup as a key, manually set its value to point to
    # the first element
    cup_dictionary[1000000] = cups[0]
    current_cup: int = 0
    destination_cup: int
    cup1: int
    cup2: int
    cup3: int
    for _ in range(10000000):
        if current_cup == 0:
            current_cup = cups[0]

        cup1 = cup_dictionary[current_cup]
        cup2 = cup_dictionary[cup1]
        cup3 = cup_dictionary[cup2]

        three_cups = [cup1, cup2, cup3]
        # to "remove" the three elements, make the current_cup
        # point to the cup after cup3 in the dictionary
        cup_dictionary[current_cup] = cup_dictionary[cup3]

        # get the destination cup
        if current_cup == 1:
            # so that we don't find the maximum by iterating over the dictionary
            destination_cup = 1000000
        else:
            destination_cup = current_cup - 1
        # now the value of the destination_cup can either by in the three_cups
        # if so, keep subtracting 1 until it finds a cup that wasn't picked up
        while destination_cup in three_cups:
            if destination_cup == 1:
                destination_cup = 1000000
            else:
                destination_cup -= 1

        # make cup 3 point where the destination cup was originally pointing
        cup_dictionary[cup3] = cup_dictionary[destination_cup]
        # make the destination cup point to cup1 now
        cup_dictionary[destination_cup] = cup1
        # cup 1 still points to cup2
        # cup 2 still points to cup 3

        # get the new current cup which is the next one
        current_cup = cup_dictionary[current_cup]

        # let's print the current order
        # we want the one after 1
    cup_we_want = cup_dictionary[1]
    cup_we_want_2 = cup_dictionary[cup_we_want]
    final: str = str(cup_we_want * cup_we_want_2)
    return final


if __name__ == "__main__":
    testinput_label: str = "389125467"
    realinput_label: str = "158937462"
    testinput: Deque[int] = deque([int(num) for num in testinput_label])
    realinput: Deque[int] = deque([int(num) for num in realinput_label])
    final: str = play_cups(realinput)
    print(final)

    # i wish we could get a hint of what's coming in part 2....
    # wouldn't use lists or deques then....
    # time to use a better structure, yay for dictionaries
    # let's see if we still get the same thing for part 1 using new method
    final = part1_with_dict(realinput_label)
    print(final)
    # yay
    # finally answer for part 2
    print(long_game_of_cups(realinput_label))
