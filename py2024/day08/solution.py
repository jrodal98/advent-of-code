#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from collections import defaultdict
from itertools import combinations


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        positions = defaultdict(list)
        for p, v in self.grid.iter(disqualify="."):
            positions[v].append(p)

        antinodes = set()
        for points in positions.values():
            for p1, p2 in combinations(points, 2):
                dx = p2.x - p1.x
                dy = p2.y - p1.y
                for p in p1, p2:
                    for m in (1, -1):
                        new_point = p.translate(m * dx, m * dy)
                        if new_point not in (p1, p2) and self.grid.inbounds(new_point):
                            antinodes.add(new_point)
        return len(antinodes)

    def _part2(self) -> Solution:
        positions = defaultdict(list)
        for p, v in self.grid.iter(disqualify="."):
            positions[v].append(p)

        antinodes = set()
        for all_points in positions.values():
            for p1, p2 in combinations(all_points, 2):
                antinodes.add(p1)
                antinodes.add(p2)
                dx = p2.x - p1.x
                dy = p2.y - p1.y
                points = [p1, p2]
                visited = set()
                while points:
                    new_points = []
                    for p in points:
                        visited.add(p)
                        for m in (1, -1):
                            new_point = p.translate(m * dx, m * dy)
                            if new_point not in visited and self.grid.inbounds(
                                new_point
                            ):
                                new_points.append(new_point)
                                antinodes.add(new_point)
                                visited.add(new_point)
                    points = new_points
        return len(antinodes)
