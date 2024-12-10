#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid
from aoc_utils.point import Point
from collections import defaultdict


class Solver(BaseSolver):
    def reachable(
        self,
        grid: Grid[int],
        start_pos: Point,
        start_val: int,
        finish: Point,
        graph: dict[Point, dict[Point, bool]],
    ) -> bool:
        if start_pos == finish:
            graph[start_pos][finish] = True
            return True

        if finish in graph[start_pos]:
            return graph[start_pos][finish]
        for neighbor_pos, neighbor_val, _ in grid.neighbors(start_pos):
            if neighbor_val - start_val != 1:
                continue
            if self.reachable(grid, neighbor_pos, neighbor_val, finish, graph):
                graph[start_pos][finish] = True
                return True

        graph[start_pos][finish] = False

        return False

    def _part1(self) -> Solution:
        grid = self.grid.transform(int)
        trailhead_positions = list(grid.findall(0))
        peak_positions = list(grid.findall(9))
        ans = 0
        graph = defaultdict(dict)
        for peak in peak_positions:
            for trailhead in trailhead_positions:
                if self.reachable(grid, trailhead, 0, peak, graph):
                    ans += 1
        return ans

    def _part2(self) -> Solution:
        raise NotImplementedError
