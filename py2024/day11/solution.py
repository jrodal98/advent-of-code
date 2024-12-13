#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from functools import cache


class Solver(BaseSolver):
    @classmethod
    @cache
    def num_stones(cls, stone: int, blinks: int) -> int:
        if blinks == 0:
            return 1

        blinks -= 1

        if stone == 0:
            return cls.num_stones(1, blinks)

        stone_str = str(stone)
        left, right = stone_str[: len(stone_str) // 2], stone_str[len(stone_str) // 2 :]
        if len(left) == len(right):
            return cls.num_stones(int(left), blinks) + cls.num_stones(
                int(right), blinks
            )

        return cls.num_stones(stone * 2024, blinks)

    def _part1(self) -> Solution:
        stones = [int(i) for i in self.data.split()]
        return sum(self.num_stones(stone, 25) for stone in stones)

    def _part2(self) -> Solution:
        blinks = 25 if self._is_unit_test else 75
        stones = [int(i) for i in self.data.split()]
        return sum(self.num_stones(stone, blinks) for stone in stones)
