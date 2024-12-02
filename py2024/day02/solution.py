#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    def _is_level_safe(self, nums: list[int]) -> bool:
        has_increased = False
        has_decreased = False
        for prev, cur in zip(nums, nums[1:]):
            diff = abs(cur - prev)
            if diff < 1 or diff > 3:
                return False

            has_increased = has_increased or cur > prev
            has_decreased = has_decreased or cur < prev

            if has_increased and has_decreased:
                return False

        return True

    def _part1(self) -> Solution:
        return sum(
            self._is_level_safe([int(n) for n in level.split()])
            for level in self.lines()
        )

    def _part2(self) -> Solution:
        return sum(
            any(
                self._is_level_safe(nums[:i] + nums[i + 1 :])
                for i in range(len(nums) + 1)
            )
            for nums in ([int(n) for n in level.split()] for level in self.lines())
        )
