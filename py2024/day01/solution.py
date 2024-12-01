#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        lines = self.data.splitlines()
        left = []
        right = []
        for line in lines:
            l, r = line.split()
            left.append(int(l))
            right.append(int(r))
        left.sort()
        right.sort()
        s = 0
        for a, b in zip(left, right):
            s += abs(a - b)
        return s

    def _part2(self) -> Solution:
        lines = self.data.splitlines()
        left = []
        right = []
        for line in lines:
            l, r = line.split()
            left.append(int(l))
            right.append(int(r))
        left.sort()
        right.sort()

        s = 0
        for a in left:
            for b in right:
                if a == b:
                    s += a
        return s
