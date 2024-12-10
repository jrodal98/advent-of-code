#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid
from aoc_utils.point import Point
from functools import cache


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return self._both()[0]

    def _part2(self) -> Solution:
        return self._both()[1]

    @cache
    def _both(self) -> tuple[int, int]:
        grid = self.grid.transform(int)
        paths = [self._score(grid, pos, val) for pos, val in grid.iter(include=0)]
        return sum(len(set(p)) for p in paths), sum(len(p) for p in paths)

    def _score(self, grid: Grid[int], pos: Point, val: int) -> list[Point]:
        return (
            [pos]
            if val == 9
            else [
                point
                for neighbor_pos, neighbor_val, _ in grid.neighbors(
                    pos, include=val + 1
                )
                for point in self._score(grid, neighbor_pos, neighbor_val)
            ]
        )
