#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.point import Point


class Solver(BaseSolver):
    def _extract_regions(self) -> list[set[Point]]:
        seen = set()
        regions = []
        for point, value in self.grid.iter(exclude=lambda p, _: p in seen):
            region = set()
            queue = [point]
            while queue:
                p = queue.pop()
                region.add(p)
                for neighbor in p.neighbors():
                    if neighbor in region:
                        continue
                    if self.grid.get(neighbor) == value:
                        queue.append(neighbor)
            seen |= region
            regions.append(region)

        return regions

    def _score_region(self, region: set[Point]) -> int:
        area = len(region)
        perimeter = area * 4
        for p in region:
            for neighbor in p.neighbors():
                if neighbor in region:
                    perimeter -= 1
        return area * perimeter

    def _part1(self) -> Solution:
        regions = self._extract_regions()
        return sum(self._score_region(r) for r in regions)

    def _part2(self) -> Solution:
        raise NotImplementedError
