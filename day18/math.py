import re
from contextlib import contextmanager
from typing import IO, ContextManager, Generator, List

"""
some of this is inspired by reddit research but hopefully
explained slightly better.
At some point I want to write a solution using AST and a
Shunting-yard algorithm.
"""


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


class ChristmasInt(int):
    """
    Let's overload some operators
    """

    def __sub__(self, other):
        return ChristmasInt(int(self) * other)

    def __add__(self, other):
        return ChristmasInt(int(self) + other)

    def __and__(self, other):
        return ChristmasInt(int(self) * other)


def parse_equation(equation: str, operator: str = "-") -> int:
    """
    Parses an equation making any necessary replacements and uses eval
    to return it.
    """
    # first replace all numbers by Christmas Integers
    equation = re.sub(r"(\d+)", r"ChristmasInt(\1)", equation)
    """
    now in part 1
    let's replace all the * (mul operator) by - (none are there)
    and then when we use the overloaded __sub__ method of our christmas int
    to make those numbers multiply. Why are we doing it this way?
    That way because there are no multiplication signs (only + and -)
    the equation evaluates left to right.
    BUT when it gets to a -  (sub operator), it multiplies the two numbers
    instead
    in part 2, we replace the * operator by the &. Why do we do that? Because
    we have also overloaded the binary and operator (since none are found in
    the expressions). what does it do? well addition is evaluated before
    multiplication and binary operator have a lower precedence in python rules
    STILL, we don't want to actually do a binary AND but 
    we still multiply the two numbers and that's what happens in the
    overloaded & operator in our Christmas Integer
    """
    equation = equation.replace("*", operator)
    """
    now use the eval method to return an integer
    let's hope there's malicious code in the input
    don't do this with code you read from files...
    you might think, oh it's fine, it's just numbers..
    but clearly you don't remember the intcode from last year!!!
    """
    return eval(equation)


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    with cm as input_file:
        equations: List[str] = [
            equation.replace(" ", "") for equation in input_file.read().splitlines()
        ]
    print(sum(map(parse_equation, equations)))
    print(sum(parse_equation(equation, "&") for equation in equations))
