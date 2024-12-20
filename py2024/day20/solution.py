#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from itertools import combinations


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        min_cheat = (
            2 if part1 and self._is_unit_test else 50 if self._is_unit_test else 100
        )
        max_cheat = 2 if part1 else 20
        return sum(
            (
                (cheat := n1.manhattan_distance(n2)) <= max_cheat
                and cheat <= (b - a) - min_cheat
            )
            for (a, n1), (b, n2) in combinations(
                enumerate(self.grid.shortest_path("S", "E", exclude="#")), 2
            )
        )
