from collections import defaultdict
from contextlib import contextmanager
from typing import IO, ContextManager, DefaultDict, Dict, Generator, List, Set, Tuple


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def find_safe_ingredients(
    recipes: List[Set[str]],
    possible_allergens: DefaultDict[str, Set[str]],
    recipes_containing: DefaultDict[str, List[int]],
) -> List[str]:
    """
    This function goes through the recipes, possible allergens and recipes containing
    data and returns the safe ingredients.
    """
    safe_ingredients: List[str] = []

    for ingredient, poss_allergens in possible_allergens.items():
        impossibilities: Set[str] = set()
        for allergen in poss_allergens:
            if any(
                ingredient not in recipes[recipe_index]
                for recipe_index in recipes_containing[allergen]
            ):
                impossibilities.add(allergen)

        # let's now look at the differences between the possibilities
        # and impossibilities
        poss_allergens -= impossibilities
        # if there are no possible allergens, it means it's a safe ingredient
        # with no allergens
        if not poss_allergens:
            safe_ingredients.append(ingredient)
    return safe_ingredients


def match_allergen_ingredients(
    possible_allergens: DefaultDict[str, Set[str]]
) -> Dict[str, str]:
    """
    This function goes through the allergens and matches them with the ingredient that
    has the respective allergen.
    """
    allergen_dictionary: Dict[str, str] = {}

    # now iterate through all the possible allergens left
    # and look for the shortest set
    while possible_allergens:
        for ingredient, allergens in possible_allergens.items():
            if len(allergens) == 1:
                break
        allergen = allergens.pop()
        allergen_dictionary[allergen] = ingredient
        del possible_allergens[ingredient]

        for ingredient, allergens in possible_allergens.items():
            if allergen in allergens:
                allergens.remove(allergen)
    return allergen_dictionary


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    recipes: List[Set[str]] = []
    possible_allergens: DefaultDict[str, Set[str]] = defaultdict(set)
    recipes_containing: DefaultDict[str, List[int]] = defaultdict(list)

    with cm as input_file:
        for index, line in enumerate(input_file.read().splitlines()):
            unprocessed_ingredients, unprocessed_allergens = line.rstrip(")\n").split(" (contains ")
            ingredients: Set[str] = set(unprocessed_ingredients.split())
            allergens: Set[str] = set(unprocessed_allergens.split(", "))
            recipes.append(ingredients)

            for allergen in allergens:
                recipes_containing[allergen].append(index)
            for ingredient in ingredients:
                possible_allergens[ingredient] |= allergens

    # get the safe ingredients
    safe_ingredients: List[str] = find_safe_ingredients(
        recipes, possible_allergens, recipes_containing
    )

    # now let's count the safe ingredients
    total: int = 0
    for ingredient in safe_ingredients:
        total += sum(ingredient in recipe for recipe in recipes)
    print(total)

    # part 2
    # clean the possible_allergens by removing the safe ingredients
    for ingredient in safe_ingredients:
        del possible_allergens[ingredient]
    allergen_dictionary: Dict[str, str] = match_allergen_ingredients(possible_allergens)
    print(",".join(map(allergen_dictionary.get, sorted(allergen_dictionary))))
