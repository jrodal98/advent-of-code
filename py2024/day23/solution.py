#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
import networkx as nx


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        graph = nx.Graph([(line[:2], line[3:]) for line in self.lines()])
        if part1:
            return sum(
                len(clique) == 3 and any(pc.startswith("t") for pc in clique)
                for clique in nx.enumerate_all_cliques(graph)
            )
        else:
            return ",".join(sorted(max(nx.find_cliques(graph), key=len)))
