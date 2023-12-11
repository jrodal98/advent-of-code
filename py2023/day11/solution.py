#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid

from itertools import combinations


class Solver(BaseSolver):
    def _get_galaxy_positions(self) -> list[tuple[int, int]]:
        rows = []
        for row in self.data.splitlines():
            if "#" not in row:
                rows.append(row)
            rows.append(row)

        t_rows = Grid(rows).transpose().rows
        rows = []
        for row in t_rows:
            if "#" not in row:
                rows.append(row)
            rows.append(row)

        grid = Grid(rows).transpose()

        galaxy_positions = []
        for y in range(grid.h):
            for x in range(grid.w):
                cell = grid.at(x, y)
                if cell == "#":
                    galaxy_positions.append((x, y))

        return galaxy_positions

    def _part1(self) -> Solution:
        galaxy_positions = self._get_galaxy_positions()
        res = 0
        for (x1, y1), (x2, y2) in combinations(galaxy_positions, 2):
            res += abs(x1 - x2) + abs(y1 - y2)
        return res

    def _part2(self) -> Solution:
        raise NotImplementedError
