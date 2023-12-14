#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        grid = Grid.from_lines(self.data)
        for _ in range(grid.h):
            for p, c in grid.iter():
                if c == "O" and grid.up(p) == ".":
                    grid.replace(p.up, "O")
                    grid.replace(p, ".")
        ans = 0
        for j, row in enumerate(grid.rows()):
            for i in row:
                if i == "O":
                    ans += grid.h - j
        return ans

    def _part2(self) -> Solution:
        raise NotImplementedError
