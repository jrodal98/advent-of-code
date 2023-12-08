#!/usr/bin/env python3
# www.jrodal.com

from collections import Counter
from aoc_utils.base_solver import BaseSolver, Solution


def score_hand(s: str) -> int:
    letters = Counter(s)

    if max(letters.values()) == 5:
        # Five of a kind
        return -1
    elif max(letters.values()) == 4:
        # Four of a kind
        return -2
    elif max(letters.values()) == 3:
        # Full house
        if len(letters) == 2:
            return -3
        # Three of a kind
        else:
            return -4
    elif max(letters.values()) == 2:
        # Two pair
        if len(letters) == 3:
            return -5
        # One pair
        else:
            return -6
    else:
        # High card
        return -7


def hand_sorter(s: str, wildcard_jokers: bool = False):
    card_scores = {
        "A": 13,
        "K": 12,
        "Q": 11,
        "J": 10,
        "T": 9,
        "9": 8,
        "8": 7,
        "7": 6,
        "6": 5,
        "5": 4,
        "4": 3,
        "3": 2,
        "2": 1,
    }
    if not wildcard_jokers:
        hand_score = score_hand(s)
        return [hand_score] + [card_scores[letter] for letter in s]

    card_scores["J"] = 0

    if "J" in s:
        hands = [s.replace("J", c) for c in card_scores.keys()]
    else:
        hands = [s]
    return [max(score_hand(h) for h in hands)] + [card_scores[letter] for letter in s]


class Solver(BaseSolver):
    PART1_EXAMPLE_SOLUTION: Solution | None = 6440
    PART2_EXAMPLE_SOLUTION: Solution | None = 5905

    def compute_answer(self, wildcard_jokers: bool = False) -> Solution:
        hands = []
        bids = []
        for line in self.data.splitlines():
            hand, bid = line.split()
            bid = int(bid)
            hands.append(hand)
            bids.append(bid)

        sorted_hands = sorted(
            zip(hands, bids),
            key=lambda y: hand_sorter(y[0], wildcard_jokers=wildcard_jokers),
            reverse=False,
        )
        res = 0
        for i, (hand, bid) in enumerate(sorted_hands, 1):
            res += i * bid
        return res

    def _part1(self) -> Solution:
        return self.compute_answer(wildcard_jokers=False)

    def _part2(self) -> Solution:
        return self.compute_answer(wildcard_jokers=True)
