from contextlib import contextmanager
from typing import IO, ContextManager, Dict, Generator, List


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def play_game(starting_numbers: List[int], target_turns: int) -> int:
    """
    This functions plays the game. What are the rules again?
    It's am emory game where players take turns saying numbers.
    First begin by taking turns reading from the list of starting numbers.
    Then each turn consists of the most recently said number.
    If that's the first time it's mentioned, the current player says 0.
    Otherwise, the number has been mentioned already so the current player
    says how many turns apart it is from when it was last spoken.
    For an integer `turns`, the function returns what that number
    will be or if dinner is ready and my morning coffee finished or
    sunrise happened.
    """
    # add the numbers to a dictionary, don't use lists like I did in previous years
    # the key is the number, the value is on which turn they were last spoken
    i_have_spoken: Dict[int, int] = {}
    for index, number in enumerate(starting_numbers[:-1]):
        turn: int = index + 1
        this_is_the_number: int = number
        i_have_spoken[this_is_the_number] = turn
    turn += 1
    # from the last number onwards, check if it has been said
    the_last_number: int = starting_numbers[-1]
    while turn != target_turns:
        last_one: int = the_last_number
        if last_one in i_have_spoken:
            the_last_number = (turn) - i_have_spoken[the_last_number]
        else:
            the_last_number = 0
        i_have_spoken[last_one] = turn
        turn += 1
    return the_last_number


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    with cm as input_file:
        starting_numbers: List[int] = [
            int(num) for num in input_file.readline().split(",")
        ]
    print(play_game(starting_numbers, 2020))
    print(play_game(starting_numbers, 30000000))
