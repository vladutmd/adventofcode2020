from collections import defaultdict, deque
from contextlib import contextmanager
from itertools import islice
from typing import (
    IO,
    ContextManager,
    DefaultDict,
    Deque,
    Dict,
    Generator,
    List,
    Set,
    Tuple,
)


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def play_easy_game(p1_stack: Deque[int], p2_stack: Deque[int]) -> Deque[int]:
    """
    This functions plays the game between two stacks.
    Each turn, the players draws their top card and the player
    with the higher-valued card wins the round. The winner keeps both cards
    and places them at the bottom of the deck so that the winning card is
    above the losing card.
    When a player has all the cards, they win and the game ends.
    """
    round: int = 0  # for verification purposes only
    while len(p1_stack) > 0 and len(p2_stack) > 0:
        p1_card: int = p1_stack.pop()
        p2_card: int = p2_stack.pop()
        if p1_card > p2_card:
            p1_stack.appendleft(p1_card)
            p1_stack.appendleft(p2_card)
        else:
            p2_stack.appendleft(p2_card)
            p2_stack.appendleft(p1_card)
        round += 1
    print(round)  # for verification purposes only
    return max(p1_stack, p2_stack, key=len)


def play_recursive_combat(
    p1_stack: Deque[int],
    p2_stack: Deque[int],
    previous_configurations: Set[Tuple[Tuple[int, ...], Tuple[int, ...]]],
) -> Tuple[int, Deque[int]]:
    """
    This function plays the recursive version of the game. What are the rules
    you ask? If only I understood :(
    But let's try and explain them (to myself I mean, don't care about you):
    - if in a previous round of the game where there was the same cards
    in the same order in the same players' decks, the game ends and player 1
    wins. (only consider previous rounds from this game, not from other games)
    - otherwise, this round's cards must be in a new configuration
    - as before, each round begins with the players drawing the top card of
    their game as they would in the simple game
    - if both players have at least as many cards remaining in their deck as
    the value of the card they just drew, the winner of the game is determined
    by playing a new game of recursive combat
    - otherwise, at least one player must not have enough cards left in their
    deck to play the recursie game; the winner of the round is the player with
    the higher-value card.
    This makes more sense if one looks at the example game at
     https://adventofcode.com/2020/day/22#part2
    - just like before, the winner of the round puts the two cards at the bottom
    of their deck: winning card first, losing card second.
    - note that unlike before, it doesn't mean that the winning card has a higher
    value, as a winning card could be winning because of the sub-game played
    - if a player has all the cards, they win and the game ends
    """
    winner: int
    while len(p1_stack) > 0 and len(p2_stack) > 0:
        if (tuple(p1_stack), tuple(p2_stack)) in previous_configurations:
            return 1, p1_stack
        previous_configurations.add((tuple(p1_stack), tuple(p2_stack)))

        # get a card from each stack
        p1_card: int = p1_stack.pop()
        p2_card: int = p2_stack.pop()

        # check if a sub-game should be played
        if len(p1_stack) >= p1_card and len(p2_stack) >= p2_card:
            # ah doing stacks make it annoying to copy...
            p1_stack_subgame: Deque[int] = p1_stack.copy()
            p1_stack_subgame.reverse()
            p1_stack_subgame = deque(islice(p1_stack_subgame, 0, p1_card))
            p1_stack_subgame.reverse()
            p2_stack_subgame: Deque[int] = p2_stack.copy()
            p2_stack_subgame.reverse()
            p2_stack_subgame = deque(islice(p2_stack_subgame, 0, p2_card))
            p2_stack_subgame.reverse()
            winner, _ = play_recursive_combat(p1_stack_subgame, p2_stack_subgame, set())
        else:
            winner = 1 if p1_card > p2_card else 2

        if winner == 1:
            p1_stack.appendleft(p1_card)
            p1_stack.appendleft(p2_card)
        else:
            p2_stack.appendleft(p2_card)
            p2_stack.appendleft(p1_card)
    if len(p1_stack) > 0:
        return (1, p1_stack)
    else:
        return (2, p2_stack)


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    p1_cards: Deque[int] = deque()
    p2_cards: Deque[int] = deque()

    with cm as input_file:
        p1: str
        p2: str
        p1, p2 = [block for block in input_file.read().split("\n\n")]

    for card in p1.split("\n")[::-1]:
        if card.isdigit():
            p1_cards.append(int(card))
    for card in p2.split("\n")[::-1]:
        if card.isdigit():
            p2_cards.append(int(card))

    p1_cards_part2: Deque[int] = p1_cards.copy()
    p2_cards_part2: Deque[int] = p2_cards.copy()
    winning_stack: Deque[int] = play_easy_game(p1_cards, p2_cards)
    print(sum((index + 1) * card for index, card in enumerate(winning_stack)))

    winner, _ = play_recursive_combat(p1_cards_part2, p2_cards_part2, set())
    if winner == 1:
        print(sum((index + 1) * card for index, card in enumerate(p1_cards_part2)))
    else:
        print(sum((index + 1) * card for index, card in enumerate(p2_cards_part2)))
