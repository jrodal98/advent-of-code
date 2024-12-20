#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
import networkx as nx
from aoc_utils.grid import Grid
from aoc_utils.point import Point


class Solver(BaseSolver):
    def _shortest_path_to_exit(self, bytes_falling: int) -> int:
        upper_bound = 7 if self._is_unit_test else 71
        grid = Grid(data=["."] * upper_bound * upper_bound)
        for line, _ in zip(self.lines(), range(bytes_falling)):
            x, y = map(int, line.split(","))
            grid[(x, y)] = "#"

        source = Point(0, 0)
        target = Point(upper_bound - 1, upper_bound - 1)

        return len(grid.shortest_path(source, target, exclude="#")) - 1

    def _solve(self, part1: bool) -> Solution:
        if part1:
            return self._shortest_path_to_exit(12 if self._is_unit_test else 1024)

        lines = self.lines()
        low, high = 0, len(lines) - 1

        while low <= high:
            mid = (low + high) // 2
            try:
                self._shortest_path_to_exit(mid + 1)
            except Exception:
                high = mid - 1
            else:
                low = mid + 1

        return lines[low]
