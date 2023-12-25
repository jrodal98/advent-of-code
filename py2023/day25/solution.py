#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
import networkx as nx


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        graph = nx.Graph()
        nodes = set()
        for line in self.data.splitlines():
            source, connected_to = line.split(": ")
            nodes.add(source)
            for connected in connected_to.split():
                nodes.add(connected)
                graph.add_edge(source, connected)

        for edge in nx.minimum_edge_cut(graph):
            graph.remove_edge(*edge)

        connected_components = list(nx.connected_components(graph))
        return len(connected_components[0]) * len(connected_components[1])

    def _part2(self) -> Solution:
        return 0
