#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
import networkx as nx
from aoc_utils.grid import Grid
from aoc_utils.point import Point


class Solver(BaseSolver):
    def _shortest_path_to_exit(self, bytes_falling: int) -> int:
        upper_bound = 7 if self._is_unit_test else 71
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

    def _solve(self, part1: bool) -> Solution:
        if part1:
            return self._shortest_path_to_exit(12 if self._is_unit_test else 1024)

        # for bytes_falling, byte_str in enumerate(self.lines(), start=1):
        #     try:
        #         self._shortest_path_to_exit(bytes_falling)
        #     except nx.NetworkXNoPath:
        #         return byte_str

        lines = list(self.lines())
        low, high = 0, len(lines) - 1
        result = None

        while low <= high:
            mid = (low + high) // 2
            try:
                self._shortest_path_to_exit(
                    mid + 1
                )  # Assuming this takes the index as input
            except nx.NetworkXNoPath:
                result = lines[mid]  # Record the failing value
                high = mid - 1  # Look for earlier failures
            else:
                low = mid + 1  # Look for failures later

        assert result
        return result
