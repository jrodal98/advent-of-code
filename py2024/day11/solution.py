#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.helpers import ints
from aoc_utils.base_solver import BaseSolver, Solution
from functools import cache


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        return sum(
            _num_stones(stone, 25 if part1 or self._is_unit_test else 75)
            for stone in ints(self.data)
        )


@cache
def _num_stones(stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1

    blinks -= 1

    if stone == 0:
        return _num_stones(1, blinks)

    stone_str = str(stone)
    left, right = stone_str[: len(stone_str) // 2], stone_str[len(stone_str) // 2 :]
    if len(left) == len(right):
        return _num_stones(int(left), blinks) + _num_stones(int(right), blinks)

    return _num_stones(stone * 2024, blinks)
