from contextlib import contextmanager
from typing import IO, ContextManager, Generator, List, Set


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def count_answers(group: List[str]) -> int:
    """
    This function counts the number of different answers given by each group.
    Returns an integer.
    """
    n_answers: int = 0
    unique_answers: Set[int] = set()
    for answers in group:
        for answer in answers:
            unique_answers.add(answer)
    n_answers = len(unique_answers)
    return n_answers


def count_all_answers(group: List[str]) -> int:
    """
    This functions counts the number of answers that
    everyone in a group  answered.
    """
    first_person = set(group[0])
    if len(group) > 1:
        return len(first_person.intersection(*group[1:]))
    return len(first_person)


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    with cm as input_file:
        groups: List[List[str]] = [
            j
            for j in [
                i.replace("\n", " ").split() for i in input_file.read().split("\n\n")
            ]
        ]

    count: int = 0
    for group in groups:
        count += count_answers(group)
    print(count)

    count: int = 0
    for group in groups:
        count += count_all_answers(group)
    print(count)
