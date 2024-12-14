#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.helpers import ints
from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid
from aoc_utils.point import Point


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        if self._is_unit_test:
            w = 11
            h = 7
        else:
            w = 101
            h = 103

        time = 100

        g = Grid(data=[0] * w * h, w=w, h=h)
        for line in self.lines():
            px, py, vx, vy = ints(line, include_sign=True)
            x = px + vx * time
            y = py + vy * time
            p = Point(x % w, y % h)
            v = g.get(p) or 0
            g.replace(p, v + 1)
        if self._is_unit_test:
            g.display()

        mid_x, mid_y = w // 2, h // 2
        score = 1
        for lx, ux, ly, uy in [
            (0, mid_x, 0, mid_y),
            (0, mid_x, mid_y + 1, h),
            (mid_x + 1, w, 0, mid_y),
            (mid_x + 1, w, mid_y + 1, h),
        ]:
            q = 0
            for x in range(lx, ux):
                for y in range(ly, uy):
                    q += g.at(Point(x, y))
            score *= q
        return score
