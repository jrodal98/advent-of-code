#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid
from aoc_utils.point import Direction, Point
import networkx as nx


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        graph = nx.Graph()
        for p, _ in self.grid.iter(exclude="#"):
            for neighbor_p, _, direction in self.grid.neighbors(p, exclude="#"):
                graph.add_edge((p, direction), (neighbor_p, direction), weight=1)
                graph.add_edge(
                    (p, direction), (neighbor_p, direction.clockwise), weight=1001
                )
                graph.add_edge(
                    (p, direction),
                    (neighbor_p, direction.counter_clockwise),
                    weight=1001,
                )

        source = (self.grid.find("S"), Direction.RIGHT)
        end_node = self.grid.find("E")
        target = (end_node, Direction.UPPER_RIGHT)

        for d in Direction.dir4():
            graph.add_edge((end_node, d), target, weight=0)

        if part1:
            return nx.shortest_path_length(
                graph, source=source, target=target, weight="weight"
            )
        else:
            return len(
                {
                    pos
                    for path in nx.all_shortest_paths(
                        graph, source=source, target=target, weight="weight"
                    )
                    for pos, _ in path
                }
            )
