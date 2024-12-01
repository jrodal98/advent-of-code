#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from collections import Counter


class Solver(BaseSolver):
    def _get_lists(self) -> tuple[list[int], list[int]]:
        left = []
        right = []
        for line in self.lines():
            l, r = line.split()
            left.append(int(l))
            right.append(int(r))
        left.sort()
        right.sort()
        return left, right

    def _part1(self) -> Solution:
        left, right = self._get_lists()
        return sum(abs(a - b) for a, b in zip(left, right))

    def _part2(self) -> Solution:
        left, right = self._get_lists()
        right_counts = Counter(right)
        return sum(v * right_counts[v] for v in left)
