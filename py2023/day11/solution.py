#!/usr/bin/env python3
# www.jrodal.com

from typing import Iterator
from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid, Point

from itertools import combinations


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return self._calculate_sum_of_shortest_paths(expansion=2)

    def _part2(self) -> Solution:
        return self._calculate_sum_of_shortest_paths(expansion=1_000_000)

    def _calculate_sum_of_shortest_paths(self, expansion: int) -> int:
        return sum(
            p1.manhattan_distance(p2)
            for p1, p2 in combinations(self._get_galaxy_positions(expansion), 2)
        )

    def _get_galaxy_positions(self, expansion: int = 2) -> Iterator[Point]:
        grid = Grid.from_lines(self.data)

        y_translation = [0] * grid.h
        for y, row in enumerate(grid.iter_rows()):
            if "#" not in row:
                for j in range(y, grid.h):
                    y_translation[j] += expansion - 1

        x_translation = [0] * grid.w
        for x, col in enumerate(grid.iter_cols()):
            if "#" not in col:
                for j in range(x, grid.w):
                    x_translation[j] += expansion - 1

        for p, _ in grid.iter(include="#"):
            yield p.translate(x_translation[p.x], y_translation[p.y])
