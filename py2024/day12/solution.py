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
                ############################### EXTERIOR CORNERS ####################################
                if (
                    p.left in perimeter
                    and p.down in perimeter
                    and p.bottom_left in region
                ):
                    num_sides += 1

                if (
                    p.right in perimeter
                    and p.down in perimeter
                    and p.bottom_right in region
                ):
                    num_sides += 1

                if p.left in perimeter and p.up in perimeter and p.upper_left in region:
                    num_sides += 1

                if (
                    p.right in perimeter
                    and p.up in perimeter
                    and p.upper_right in region
                ):
                    num_sides += 1

                ############################### INTERIOR CORNERS ####################################
                if p.left in region and p.down in region:
                    num_sides += 1

                if p.right in region and p.down in region:
                    num_sides += 1

                if p.left in region and p.up in region:
                    num_sides += 1

                if p.right in region and p.up in region:
                    num_sides += 1

            score += area * num_sides
        return score
