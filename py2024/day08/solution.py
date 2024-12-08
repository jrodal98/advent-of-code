#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from collections import defaultdict
from itertools import combinations
from aoc_utils.line import Line


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return self._solver(True)

    def _part2(self) -> Solution:
        return self._solver(False)

    def _solver(self, part1: bool) -> Solution:
        positions = defaultdict(list)
        for p, v in self.grid.iter(disqualify="."):
            positions[v].append(p)

        antinodes = set()
        for points in positions.values():
            for p1, p2 in combinations(points, 2):
                line = Line(p1, p2)
                antinodes |= set(
                    line.iter(
                        exclude_start=part1,
                        continue_while=self.grid.inbounds,
                        max_steps=1 if part1 else None,
                    ),
                )
        return len(antinodes)
