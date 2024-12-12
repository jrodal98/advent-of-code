#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.point import Direction, Point


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

    def _part1(self) -> Solution:
        regions = self._extract_regions()
        score = 0
        for region in regions:
            area = len(region)
            perimeter = area * 4
            for p in region:
                for neighbor in p.neighbors():
                    if neighbor in region:
                        perimeter -= 1
            score += area * perimeter
        return score

    def _part2(self) -> Solution:
        regions = self._extract_regions()
        score = 0
        for region in regions:
            area = len(region)

            perimeter: set[Point] = set()
            for p in region:
                for neighbor in p.neighbors(include_diagonal=True):
                    if neighbor not in region:
                        perimeter.add(neighbor)

            num_sides = 0
            for p in perimeter:
                for direction in Direction.dir4():
                    ############################### INTERIOR CORNERS ####################################
                    if (
                        p.neighbor(direction) in region
                        and p.neighbor(direction.clockwise) in region
                    ):
                        num_sides += 1
                    ############################### EXTERIOR CORNERS ####################################
                    if (
                        p.neighbor(direction) in perimeter
                        and p.neighbor(direction.clockwise) in perimeter
                        and p.neighbor(direction.clockwise8) in region
                    ):
                        num_sides += 1

            score += area * num_sides
        return score
