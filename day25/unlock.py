from contextlib import contextmanager
from typing import (
    IO,
    ContextManager,
    Generator,
    List,
)


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def get_loop_size(subject: int, goal: int) -> int:
    """
    This function applies the transformation rules to
    determine a loop size.
    """
    value: int = 1
    loop_size: int = 0
    while value != goal:
        value = value * subject
        value = value % 20201227
        loop_size += 1
    return loop_size


def transform_subject(subject: int, loop_size) -> int:
    """
    This function applies the transformation rules to determine
    the value of the subject after `loop_size` operations.
    """
    value: int = 1
    for _ in range(loop_size):
        value = value * subject
        value = value % 20201227
    return value


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")

    with cm as input_file:
        keys: List[int] = [int(line) for line in input_file.read().splitlines()]
    card_pubkey: int = keys[0]
    door_pubkey: int = keys[1]
    card_loop_size: int = get_loop_size(7, card_pubkey)
    door_loop_size: int = get_loop_size(7, door_pubkey)
    door_handshake: int = transform_subject(door_pubkey, card_loop_size)
    card_handshake: int = transform_subject(card_pubkey, door_loop_size)
    assert door_handshake == card_handshake
    print(door_handshake)
