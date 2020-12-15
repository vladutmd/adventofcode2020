from collections import defaultdict
from contextlib import contextmanager
from typing import (
    IO,
    ContextManager,
    DefaultDict,
    Dict,
    Generator,
    List,
    Optional,
    Tuple,
    Union,
)


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def run_program(instructions: List[List[Union[str, int]]]) -> Tuple[int, bool]:
    """
    This function executes the instructions of a program.
    """
    visited: DefaultDict[int, int] = defaultdict(int)
    acc: int = 0
    index: int = 0
    # iterate through each line, following the logic in each
    # while checking if the line hasn't been visited before
    # if it has, return value of acc
    while index < len(instructions) and not visited[index]:
        visited[index] = 1
        op: str
        arg: int
        op, arg = instructions[index]
        if op == "acc":
            acc += arg
        elif op == "jmp":
            index += arg - 1
        index += 1
        end: bool = index == len(instructions)
    return (acc, end)


def try_fixing_program(instructions: List[List[Union[str, int]]]) -> int:
    """
    This functions changes exactly one `nop` to `jmp` or `jmp` to `nop`
    at a time and sends the updated version to the `run_program` function
    with the updated code.
    Update: adding another return value from the `run_program` function
    that tells us if it is the end of the instructions list or not.
    """
    switch_instructions: Dict[str, str] = {"nop": "jmp", "jmp": "nop"}
    for index, (instruction, arg) in enumerate(instructions):
        if instruction in switch_instructions.keys():
            instructions[index][0] = switch_instructions[instruction]
            # still need to figure out how to use Callable properly for
            # annotating the function below
            acc, end = run_program(instructions)
            # can check if it's the end now, and if so, return
            # but if it isn't, we iterate to the next instruction
            # BUT
            # we just changed one of the instructions in the program
            # so it wouldn't be the same, let's change it back
            instructions[index][0] = instruction
            if end:
                return acc
    # the instruction below should never occur
    return -1


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    with cm as input_file:
        instructions: List[List[Union[str, int]]] = [
            [line.split()[0], int(line.split()[1])]
            for line in input_file.read().splitlines()
        ]
    print(run_program(instructions)[0])
    print(try_fixing_program(instructions))
