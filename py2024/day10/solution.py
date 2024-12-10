#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid
from aoc_utils.point import Point


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return self._helper(True)

    def _part2(self) -> Solution:
        return self._helper(False)

    def _score(self, grid: Grid[int], pos: Point, val: int) -> list[Point]:
        if val == 9:
            return [pos]
        paths = []
        for neighbor_pos, neighbor_val, _ in grid.neighbors(pos, qualify=val + 1):
            paths.extend(self._score(grid, neighbor_pos, neighbor_val))
        return paths

    def _helper(self, is_part_1: bool) -> int:
        grid = self.grid.transform(int)
        ans = 0
        for trailhead in grid.findall(0):
            paths = self._score(grid, trailhead, 0)
            if is_part_1:
                paths = set(paths)
            ans += len(paths)
        return ans
