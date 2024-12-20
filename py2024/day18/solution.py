#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
import networkx as nx
from aoc_utils.grid import Grid
from aoc_utils.point import Point


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        upper_bound = 7 if self._is_unit_test else 71
        bytes_falling = 12 if self._is_unit_test else 1024
        grid = Grid(data=["."] * upper_bound * upper_bound)
        for line, _ in zip(self.lines(), range(bytes_falling)):
            x, y = map(int, line.split(","))
            grid[(x, y)] = "#"

        graph = nx.Graph()
        for p, _ in grid.iter(exclude="#"):
            for neighbor_p, _, _ in grid.neighbors(p, exclude="#"):
                graph.add_edge(p, neighbor_p, weight=1)

        source = Point(0, 0)
        target = Point(upper_bound - 1, upper_bound - 1)

        return nx.shortest_path_length(
            graph, source=source, target=target, weight="weight"
        )
