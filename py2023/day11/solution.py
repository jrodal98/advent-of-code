#!/usr/bin/env python3
# www.jrodal.com

from typing import Iterator
from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid

from itertools import combinations


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return self._calculate_sum_of_shortest_paths(expansion=2)

    def _part2(self) -> Solution:
        return self._calculate_sum_of_shortest_paths(expansion=1_000_000)

    def _calculate_sum_of_shortest_paths(self, expansion: int) -> int:
        return sum(
            Grid.taxicab_distance(*p1, *p2)
            for p1, p2 in combinations(self._get_galaxy_positions(expansion), 2)
        )

    def _get_galaxy_positions(self, expansion: int = 2) -> Iterator[tuple[int, int]]:
        grid = Grid.from_lines(self.data)
        x_translation = [0] * grid.w
        y_translation = [0] * grid.h
        for g, translation in (
            (grid, y_translation),
            (grid.transpose(), x_translation),
        ):
            for y, row in enumerate(g.rows):
                if "#" not in row:
                    for j in range(y, g.h):
                        translation[j] += expansion - 1

        for y in range(grid.h):
            for x in range(grid.w):
                cell = grid.at(x, y)
                if cell == "#":
                    yield x + x_translation[x], y + y_translation[y]
