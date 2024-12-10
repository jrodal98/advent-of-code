#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid
from aoc_utils.point import Point
from collections import defaultdict


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return self._helper(False)

    def _part2(self) -> Solution:
        return self._helper(True)

    def _score(self, grid: Grid[int], pos: Point, val: int) -> tuple[set[Point], int]:
        if val == 9:
            return {pos}, 1
        num_paths = 0
        paths = set()
        for neighbor_pos, neighbor_val, _ in grid.neighbors(pos, qualify=val + 1):
            path, score = self._score(grid, neighbor_pos, neighbor_val)
            num_paths += score
            paths |= path
        return paths, num_paths

    def _helper(self, is_part_2: bool) -> int:
        grid = self.grid.transform(int)
        ans = 0
        for trailhead in grid.findall(0):
            paths, score = self._score(grid, trailhead, 0)
            if is_part_2:
                ans += score
            elif score:
                ans += len(paths)
        return ans
