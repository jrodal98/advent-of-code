#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Point

import sys

sys.setrecursionlimit(1000000)


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        last_position = Point(0, 0)
        positions = [last_position]
        total_distance = 0
        for line in self.data.splitlines():
            d, n, _ = line.split()
            n = int(n)
            total_distance += n
            match d:
                case "R":
                    last_position = last_position + Point(n, 0)
                case "L":
                    last_position = last_position - Point(n, 0)
                case "U":
                    last_position = last_position + Point(0, n)
                case "D":
                    last_position = last_position - Point(0, n)
                case _:
                    assert False
            positions.append(last_position)

        shoelace = positions + [positions[0]]

        area = 0
        for a, b in zip(shoelace, shoelace[1:]):
            area += (a.x * b.y) - (a.y * b.x)
        return int(abs(area) / 2 + total_distance / 2 + 1)

    def _part2(self) -> Solution:
        raise NotImplementedError
