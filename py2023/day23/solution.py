#!/usr/bin/env python3
# www.jrodal.com

from rich.progress import track
from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Direction, Grid, Point
import networkx as nx
from collections import deque

import sys

sys.setrecursionlimit(100000000)


class Solver(BaseSolver):
    def _part1(
        self,
        grid: Grid[str] | None = None,
        current_position: Point = Point(1, 0),
        visited: Grid[bool] | None = None,
        steps: int = 0,
    ) -> Solution:
        grid = grid or self.grid.transform(lambda v: v.replace(".", "><^v"))
        visited = visited or grid.transform(lambda _: False)

        if current_position == Point(grid.w - 2, grid.h - 1):
            return steps

        longest_path_length = -1
        visited.replace(current_position, True)
        for dir_string in grid.at(current_position):
            new_position = current_position.neighbor(Direction.from_str(dir_string))
            if (
                not visited.get(new_position, True)
                and grid.get(new_position, "#") != "#"
            ):
                longest_path_length = max(
                    longest_path_length,
                    self._part1(grid, new_position, visited, steps + 1),
                )
        visited.replace(current_position, False)
        return longest_path_length

    def _part2(self) -> Solution:
        junctions = {Point(1, 0), Point(self.grid.w - 2, self.grid.h - 1)}
        for source, _ in self.grid.iter(disqualify="#"):
            if len(list(self.grid.neighbors(source, disqualify="#"))) > 2:
                junctions.add(source)

        graph = nx.DiGraph()
        for source in junctions:
            queue: deque[tuple[Point, int]] = deque([(source, 0)])
            seen = set()
            while queue:
                current_pos, dist = queue.popleft()
                if current_pos in seen:
                    continue
                seen.add(current_pos)
                if current_pos != source and current_pos in junctions:
                    graph.add_edge(source, current_pos, weight=dist)
                    continue
                for neighbor_p, _, _ in self.grid.neighbors(
                    current_pos, disqualify="#"
                ):
                    queue.append((neighbor_p, dist + 1))

        all_paths = nx.all_simple_paths(
            graph, Point(1, 0), Point(self.grid.w - 2, self.grid.h - 1)
        )
        ans = 0
        for p in track(all_paths):
            ans = max(ans, nx.path_weight(graph, p, weight="weight"))
        return ans
