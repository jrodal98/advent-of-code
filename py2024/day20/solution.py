#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
import networkx as nx
from aoc_utils.point import Point


class Solver(BaseSolver):
    def _shortest_path(
        self,
        graph: nx.Graph,
        start: Point,
        end: Point,
        cheat_edge: tuple[Point, Point] | None,
    ) -> int:
        if cheat_edge:
            graph.add_edge(*cheat_edge, weight=2)
        shortest_path = nx.shortest_path_length(graph, source=start, target=end)
        if cheat_edge:
            graph.remove_edge(*cheat_edge)
        return shortest_path

    def _solve(self, part1: bool) -> Solution:
        cheat_min_save = 2 if self._is_unit_test else 100

        graph = nx.Graph()
        cheat_edges = []
        for p, _ in self.grid.iter(exclude="#"):
            for neighbor_p, neighbor_v, neighbor_dir in self.grid.neighbors(p):
                if neighbor_v != "#":
                    graph.add_edge(p, neighbor_p, weight=1)
                elif self.grid.get(neighbor_p + neighbor_dir, "#") != "#":
                    if (neighbor_p + neighbor_dir, p) not in cheat_edges:
                        cheat_edges.append((p, neighbor_p + neighbor_dir))

        start = self.grid.find("S")
        target = self.grid.find("E")

        no_cheat_shortest_path = self._shortest_path(graph, start, target, None)
        ans = 0
        for edge in cheat_edges:
            if (
                self._shortest_path(graph, start, target, edge)
                <= no_cheat_shortest_path - cheat_min_save
            ):
                ans += 1
        return ans
