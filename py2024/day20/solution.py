#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from itertools import combinations


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        return sum(
            1
            for (a, n1), (b, n2) in combinations(
                enumerate(self.grid.shortest_path("S", "E", exclude="#")), 2
            )
            if b - a
            > (
                cheat_min_save := 2
                if part1 and self._is_unit_test
                else 50
                if self._is_unit_test
                else 100
            )
            and (
                (cheat_length := n1.manhattan_distance(n2)) <= (2 if part1 else 20)
                and cheat_length <= (b - a) - cheat_min_save
            )
        )
