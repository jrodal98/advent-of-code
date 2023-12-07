#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


CARD_SCORES = {
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

PART_2_CARD_SCORES = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 0,
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


def score_func(s: str) -> int:
    set_s = set(s)
    letters = {letter: s.count(letter) for letter in set_s}

    if max(letters.values()) == 5:
        return 20
    elif max(letters.values()) == 4:
        return 19
    elif max(letters.values()) == 3:
        if len(set_s) == 2:
            return 18
        else:
            return 17
    elif max(letters.values()) == 2:
        if len(set_s) == 3:
            return 16
        else:
            return 15
    else:
        return 14


def part_2_custom_sort(s: str):
    if "J" in s:
        hand_score = max([score_func(s.replace("J", c)) for c in CARD_SCORES.keys()])
    else:
        hand_score = score_func(s)
    return [hand_score] + [PART_2_CARD_SCORES[letter] for letter in s]


def custom_sort(s: str):
    hand_score = score_func(s)
    return [hand_score] + [CARD_SCORES[letter] for letter in s]


class Solver(BaseSolver):
    PART1_EXAMPLE_SOLUTION: Solution | None = 6440
    PART2_EXAMPLE_SOLUTION: Solution | None = 5905

    def part1(self) -> Solution:
        hands = []
        bids = []
        for line in self.data.splitlines():
            hand, bid = line.split()
            bid = int(bid)
            hands.append(hand)
            bids.append(bid)

        sorted_hands = sorted(
            zip(hands, bids), key=lambda y: custom_sort(y[0]), reverse=False
        )
        res = 0
        for i, (hand, bid) in enumerate(sorted_hands, 1):
            print(i, hand)
            res += i * bid
        return res

    def part2(self) -> Solution:
        hands = []
        bids = []
        for line in self.data.splitlines():
            hand, bid = line.split()
            bid = int(bid)
            hands.append(hand)
            bids.append(bid)

        sorted_hands = sorted(
            zip(hands, bids), key=lambda y: part_2_custom_sort(y[0]), reverse=False
        )
        res = 0
        for i, (hand, bid) in enumerate(sorted_hands, 1):
            print(i, hand)
            res += i * bid
        return res
