#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
import networkx as nx


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        cheat_min_save = (
            2 if part1 and self._is_unit_test else 50 if self._is_unit_test else 100
        )
        max_cheat_length = 2 if part1 else 20

        graph = nx.Graph()
        for p, _ in self.grid.iter(exclude="#"):
            for neighbor_p, _, _ in self.grid.neighbors(p, exclude="#"):
                graph.add_edge(p, neighbor_p, weight=1)

        path = nx.shortest_path(
            graph, source=self.grid.find("S"), target=self.grid.find("E")
        )

        graph = nx.Graph()
        ans = 0
        for a, n1 in enumerate(path):
            for path_length, n2 in enumerate(
                path[a + 1 + cheat_min_save :], start=cheat_min_save + 1
            ):
                steps = n1.manhattan_distance(n2)
                if steps <= max_cheat_length and path_length - steps >= cheat_min_save:
                    ans += 1

        return ans
