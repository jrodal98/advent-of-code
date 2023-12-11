#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid

from itertools import combinations


class Solver(BaseSolver):
    def _get_galaxy_positions(self, expansion: int = 2) -> list[tuple[int, int]]:
        grid = Grid.from_lines(self.data)
        grid_t = grid.transpose()
        y_translation = [0 for y in range(grid.h)]
        for y, row in enumerate(grid.rows):
            if "#" not in row:
                for j in range(y, grid.h):
                    y_translation[j] += expansion - 1

        x_translation = [0 for x in range(grid_t.h)]
        for y, row in enumerate(grid_t.rows):
            if "#" not in row:
                for j in range(y, grid_t.h):
                    x_translation[j] += expansion - 1

        galaxy_positions = []
        for y in range(grid.h):
            for x in range(grid.w):
                cell = grid.at(x, y)
                if cell == "#":
                    galaxy_positions.append(
                        (x + x_translation[x], y + y_translation[y])
                    )

        return galaxy_positions

    def _part1(self) -> Solution:
        galaxy_positions = self._get_galaxy_positions()
        res = 0
        for (x1, y1), (x2, y2) in combinations(galaxy_positions, 2):
            res += abs(x1 - x2) + abs(y1 - y2)
        return res

    def _part2(self) -> Solution:
        galaxy_positions = self._get_galaxy_positions(1_000_000)
        res = 0
        for (x1, y1), (x2, y2) in combinations(galaxy_positions, 2):
            res += abs(x1 - x2) + abs(y1 - y2)
        return res
