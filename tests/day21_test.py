import os
from collections import defaultdict
from contextlib import contextmanager
from typing import IO, ContextManager, DefaultDict, Dict, Generator, List, Set, Tuple

import pytest

from ..day21.recipe import file_read, find_safe_ingredients, match_allergen_ingredients


@pytest.fixture
def part1_input() -> Tuple[
    Dict[int, List[str]], DefaultDict[str, Set[str]], DefaultDict[str, List[int]]
]:
    """
    Returns the recipes, possible_allergens and recipes_contanining.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    recipes: List[Set[str]] = []
    possible_allergens: DefaultDict[str, Set[str]] = defaultdict(set)
    recipes_containing: DefaultDict[str, List[int]] = defaultdict(list)
    cm: ContextManager[IO] = file_read(dir_path + "/testinputs/day21")
    with cm as input_file:
        for index, line in enumerate(input_file.read().splitlines()):
            unprocessed_ingredients, unprocessed_allergens = line.rstrip(")\n").split(
                " (contains "
            )
            ingredients: Set[str] = set(unprocessed_ingredients.split())
            allergens: Set[str] = set(unprocessed_allergens.split(", "))
            recipes.append(ingredients)

            for allergen in allergens:
                recipes_containing[allergen].append(index)
            for ingredient in ingredients:
                possible_allergens[ingredient] |= allergens
    return (recipes, possible_allergens, recipes_containing)


def test_part1_safe_ingredients(
    part1_input: Tuple[
        Dict[int, List[str]], DefaultDict[str, Set[str]], DefaultDict[str, List[int]]
    ]
):
    """
    Tests the `find_safe_ingredients` function.
    """
    recipes: List[Set[str]]
    possible_allergens: DefaultDict[str, Set[str]]
    recipes_containing: DefaultDict[str, List[int]]
    recipes, possible_allergens, recipes_containing = part1_input
    safe_ingredients: List[str] = find_safe_ingredients(
        recipes, possible_allergens, recipes_containing
    )
    total: int = 0
    for ingredient in safe_ingredients:
        total += sum(ingredient in recipe for recipe in recipes)
    assert total == 5


def test_part2_match_allergens(
    part1_input: Tuple[
        Dict[int, List[str]], DefaultDict[str, Set[str]], DefaultDict[str, List[int]]
    ]
):
    """
    Tests the `match_allergen_ingreidents` function.
    """
    recipes: List[Set[str]]
    possible_allergens: DefaultDict[str, Set[str]]
    recipes_containing: DefaultDict[str, List[int]]
    recipes, possible_allergens, recipes_containing = part1_input
    safe_ingredients: List[str] = find_safe_ingredients(
        recipes, possible_allergens, recipes_containing
    )
    for ingredient in safe_ingredients:
        del possible_allergens[ingredient]
    allergen_dictionary: Dict[str, str] = match_allergen_ingredients(possible_allergens)
    assert (
        ",".join(map(allergen_dictionary.get, sorted(allergen_dictionary)))
        == "mxmxvkd,sqjhc,fvjkl"
    )
