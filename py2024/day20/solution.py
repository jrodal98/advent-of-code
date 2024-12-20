#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
import networkx as nx


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        if self._is_unit_test:
            cheat_min_save = 2 if part1 else 50
        else:
            cheat_min_save = 100

        if part1:
            max_cheat_length = 2
        else:
            max_cheat_length = 20

        graph = nx.Graph()
        for p, _ in self.grid.iter(exclude="#"):
            for neighbor_p, _, _ in self.grid.neighbors(p, exclude="#"):
                graph.add_edge(p, neighbor_p, weight=1)

        cheat_edges = {}
        for p, _ in self.grid.iter(exclude="#"):
            for reachable_p, steps in self.grid.reachable(
                p,
                max_steps=max_cheat_length,
                min_steps=2,
            ):
                if (
                    self.grid[reachable_p] != "#"
                    and (reachable_p, p) not in cheat_edges
                ):
                    cheat_edges[(p, reachable_p)] = min(
                        steps, cheat_edges.get((p, reachable_p), 100000000000)
                    )
        return sum(
            1
            for (start, end), steps in cheat_edges.items()
            if (nx.shortest_path_length(graph, source=start, target=end) - steps)
            >= cheat_min_save
        )
