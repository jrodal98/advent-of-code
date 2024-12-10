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

    def _reachable(
        self,
        grid: Grid[int],
        start_pos: Point,
        start_val: int,
        finish: Point,
        graph: dict[Point, dict[Point, int]],
    ) -> int:
        if start_pos == finish:
            graph[start_pos][finish] = 1
            return 1

        if finish in graph[start_pos]:
            return graph[start_pos][finish]

        graph[start_pos][finish] = 0
        for neighbor_pos, neighbor_val, _ in grid.neighbors(start_pos):
            if neighbor_val - start_val != 1:
                continue
            graph[start_pos][finish] += self._reachable(
                grid, neighbor_pos, neighbor_val, finish, graph
            )

        return graph[start_pos][finish]

    def _helper(self, is_part_2: bool) -> int:
        grid = self.grid.transform(int)
        trailhead_positions = list(grid.findall(0))
        peak_positions = list(grid.findall(9))
        ans = 0
        graph = defaultdict(dict)
        for peak in peak_positions:
            for trailhead in trailhead_positions:
                score = self._reachable(grid, trailhead, 0, peak, graph)
                if is_part_2:
                    ans += score
                elif score:
                    ans += 1
        return ans
