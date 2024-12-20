#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
import networkx as nx
from aoc_utils.point import Point, Direction
from time import time


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

        cheat_edges = []
        seen_edges = set()
        graph_creation_start = time()
        for p, _ in self.grid.iter(exclude="#"):
            for reachable_p, steps in self.grid.reachable(
                p,
                max_steps=max_cheat_length,
                min_steps=2,
                exclude=lambda x, c: c == "." and p.manhattan_distance(x) == 1,
            ):
                if self.grid[reachable_p] != "#" and (p, reachable_p) not in seen_edges:
                    seen_edges.add((p, reachable_p))
                    seen_edges.add((reachable_p, p))
                    cheat_edges.append((p, reachable_p, steps))
        graph_creation_end = time()

        print(f"{graph_creation_end - graph_creation_start:.3f} sec")

        ans = 0
        path_checking_start = time()
        for start, end, steps in cheat_edges:
            if (
                nx.shortest_path_length(graph, source=start, target=end) - steps
                >= cheat_min_save
            ):
                ans += 1
        path_checking_end = time()
        print(f"{path_checking_end - path_checking_start:.3f} sec")
        return ans
