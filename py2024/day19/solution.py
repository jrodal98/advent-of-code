#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from functools import cache


class Solver(BaseSolver):
    @classmethod
    @cache
    def _num_ways(cls, towel_patterns: frozenset[str], design: str) -> int:
        return (
            1
            if not design
            else sum(
                cls._num_ways(towel_patterns, design[len(pattern) :])
                for pattern in towel_patterns
                if design.startswith(pattern)
            )
        )

    def _solve(self, part1: bool) -> Solution:
        towel_patterns, desired_designs = self.sections()
        towel_patterns = frozenset(towel_patterns.split(", "))

        part1_ans = 0
        part2_ans = 0
        for design in desired_designs.split("\n"):
            num_ways = self._num_ways(towel_patterns, design)
            part1_ans += bool(num_ways)
            part2_ans += num_ways

        if part1:
            return part1_ans
        else:
            return part2_ans
