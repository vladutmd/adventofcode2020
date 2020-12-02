from contextlib import contextmanager
from typing import IO, ContextManager, Generator, List


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


cm: ContextManager[IO] = file_read("input")


with cm as input_file:
    data: List[str] = input_file.read().splitlines()


def process_password(password: str) -> bool:
    """
    Processes a password line, for example:
    1-3 a: abcde and returns whether the
    password is valid, i.e. is the letter a
    found between 1-3 times (includes) in the
    password.

    :password: str

    """
    split: List[str] = password.split(" ")
    range_values: List[int] = [int(i) for i in split[0].split("-")]
    range_values[1] += 1
    letter: str = split[1][0]
    pass_to_check: str = split[2]
    if pass_to_check.count(letter) in range(*range_values):
        return True
    return False


count: int = 0
for password in data:
    count += process_password(password)
print(count)


def updated_password_check(password: str) -> bool:
    """
    Processes a password line, for example:
    1-3 a: abcde and returns whether the
    password is valid, i.e. is the letter a
    found at positions 1 or 3 but not at both.
    The positions are indexed with a starting index of 1, not 0.
    Nice XOR ^ condition, don't think I've used it much before.

    :password: str

    """
    split: List[str] = password.split(" ")
    pos: List[int] = [int(i) - 1 for i in split[0].split("-")]
    letter: str = split[1][0]
    pass_to_check: str = split[2]

    if (pass_to_check[pos[0]] == letter) ^ (pass_to_check[pos[1]] == letter):
        return True
    return False


updated_count: int = 0
for password in data:
    updated_count += updated_password_check(password)
print(updated_count)
