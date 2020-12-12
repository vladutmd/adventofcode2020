from contextlib import contextmanager
from math import cos, pi, sin
from operator import add
from typing import IO, ContextManager, Dict, Generator, List, Optional, Tuple


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def travel(instructions: List[Tuple[str, int]]) -> Tuple[Tuple[int, int], str]:
    """
    This function accepts instructions and moves the ship in the
    right direction.
    Returns the final position and direction it is facing.
    """
    pos: List[int] = [0, 0]  # first number represents north-south
    # second number represents east-west
    facing: str = "E"
    for (action, value) in instructions:
        if action in ["N", "E", "S", "W", "F"]:
            move(action, value, pos, facing)
        elif action in ["L", "R"]:
            facing = rotate(action, value, facing)
    return ((pos[0], pos[1]), facing)


def rotate(action: str, value: int, facing: str) -> str:
    """
    This function rotates and returns a new facing direction.
    """
    directions: List[str] = ["E", "S", "W", "N"]
    current_dir: int = directions.index(facing)
    # if R, add to the index
    # if L, remove from the index
    turns: int = int(value / 90)
    if action == "L":
        return directions[int((current_dir - turns) % 4)]
    return directions[int((current_dir + turns) % 4)]


def move(action: str, value: int, pos: List[int], facing: str):
    """
    Moves N, S, E, W, F and returns the new position.
    """
    if action == "N":
        pos[0] -= value
    elif action == "S":
        pos[0] += value
    elif action == "E":
        pos[1] += value
    elif action == "W":
        pos[1] -= value
    elif action == "F":
        move(action=facing, value=value, pos=pos, facing=facing)


def travel_with_waypoint(instructions: List[Tuple[str, int]]) -> Tuple[int, int]:
    """"""
    ship_pos: List[int] = [0, 0]  # first number represents north-south
    # second number represents east-west
    waypoint_dif: List[int] = [-1, 10]  # waypoint is 10 E and 1 N
    for (action, value) in instructions:
        if action in ["N", "E", "S", "W"]:
            move_waypoint(action, value, waypoint_dif)
        elif action in ["R", "L"]:
            rotate_waypoint(action, value, waypoint_dif)
        else:
            move_ship(value, ship_pos, waypoint_dif)
    return (ship_pos[0], ship_pos[1])


def move_ship(value: int, ship_pos: List[int], waypoint_dif: List[int]):
    """
    This function moves the ship in the direction of the waypoint
    """
    ship_pos[0] = ship_pos[0] + value * waypoint_dif[0]
    ship_pos[1] = ship_pos[1] + value * waypoint_dif[1]


def move_waypoint(action: str, value: int, waypoint_dif: List[int]):
    """
    Moves N, S, E, W.
    """
    if action == "N":
        waypoint_dif[0] -= value
    elif action == "S":
        waypoint_dif[0] += value
    elif action == "E":
        waypoint_dif[1] += value
    elif action == "W":
        waypoint_dif[1] -= value


def rotate_waypoint(action: str, value: int, waypoint_dif: List[int]):
    """
    Rotates the waypoint around the ship. R clockwise and L
    anticlockwise.
    """
    # rotation matrix around origin (ship) anticlockwise with angle theta
    # x' = x cos(theta) - y sin(theta)
    # y' = x sin(theta) + y cos(theta)
    # rotate them
    x: int = waypoint_dif[0]
    y: int = waypoint_dif[1]
    sign: int = 1
    if action == "R":
        sign *= -1
    theta: float = value * pi / 180
    # rotate the coordinates
    x_rot = x * cos(sign * theta) - y * sin(sign * theta)
    y_rot = x * sin(sign * theta) + y * cos(sign * theta)
    waypoint_dif[0] = round(x_rot)
    waypoint_dif[1] = round(y_rot)


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    with cm as input_file:
        instructions: List[Tuple[str, int]] = [
            (line[0], int(line[1:])) for line in input_file.read().splitlines()
        ]
    # print(instructions)
    pos, facing = travel(instructions)
    distance: int = abs(pos[0]) + abs(pos[1])
    print(distance)
    updated_pos = travel_with_waypoint(instructions)
    updated_distance: int = abs(updated_pos[0]) + abs(updated_pos[1])
    print(updated_distance)
