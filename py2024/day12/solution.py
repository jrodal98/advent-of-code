#!/usr/bin/env python3
# www.jrodal.com

from collections.abc import Iterator
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

    @classmethod
    def _extract_perimeter(
        cls, region: set[Point], include_diagonal: bool = False
    ) -> Iterator[Point]:
        return (
            neighbor
            for p in region
            for neighbor in p.neighbors(include_diagonal=include_diagonal)
            if neighbor not in region
        )

    @classmethod
    def _extract_corners(cls, region: set[Point]) -> Iterator[Point]:
        perimeter = set(cls._extract_perimeter(region, include_diagonal=True))

        for p in perimeter:
            for direction in Direction.dir4():
                ############################### INTERIOR CORNERS ####################################
                if (
                    p.neighbor(direction) in region
                    and p.neighbor(direction.clockwise) in region
                ):
                    yield p
                ############################### EXTERIOR CORNERS ####################################
                if (
                    p.neighbor(direction) in perimeter
                    and p.neighbor(direction.clockwise) in perimeter
                    and p.neighbor(direction.clockwise8) in region
                ):
                    yield p

    def _compute_score(self, scoring_function) -> int:
        regions = self._extract_regions()
        return sum(
            len(region) * len(list(scoring_function(region))) for region in regions
        )

    def _part1(self) -> Solution:
        return self._compute_score(scoring_function=self._extract_perimeter)

    def _part2(self) -> Solution:
        return self._compute_score(scoring_function=self._extract_corners)
