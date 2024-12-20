#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
import networkx as nx
from aoc_utils.point import Point, Direction


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        cheat_min_save = 2 if self._is_unit_test else 100

        graph = nx.Graph()
        cheat_edges = []
        for p, _ in self.grid.iter(exclude="#"):
            for neighbor_p, neighbor_v, neighbor_dir in self.grid.neighbors(p):
                if neighbor_v != "#":
                    graph.add_edge(p, neighbor_p, weight=1)
                elif self.grid.get(neighbor_p + neighbor_dir, "#") != "#":
                    if (neighbor_p + neighbor_dir, p, 2) not in cheat_edges:
                        cheat_edges.append((p, neighbor_p + neighbor_dir, 2))

        ans = 0
        for start, end, time in cheat_edges:
            if (
                nx.shortest_path_length(graph, source=start, target=end) - time
                >= cheat_min_save
            ):
                ans += 1
        return ans
