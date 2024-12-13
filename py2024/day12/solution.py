#!/usr/bin/env python3
# www.jrodal.com

from collections.abc import Iterator
from typing import Callable
from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.point import Direction, Point


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        return self._compute_score(
            scoring_function=self._extract_perimeter if part1 else self._extract_corners
        )

    def _compute_score(
        self, scoring_function: Callable[[set[Point]], Iterator[Point]]
    ) -> int:
        return sum(
            len(region) * len(list(scoring_function(region)))
            for region in self._extract_regions()
        )

    def _extract_regions(self) -> Iterator[set[Point]]:
        seen = set()
        for region_start, value in self.grid.iter(exclude=lambda p, _: p in seen):
            region = set()
            queue = [region_start]
            while queue:
                point = queue.pop()
                region.add(point)
                queue.extend(
                    [
                        neighbor_p
                        for neighbor_p, _, _ in self.grid.neighbors(
                            point, exclude=lambda p, v: p in region or v != value
                        )
                    ]
                )

            seen |= region
            yield region

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
                ############################### EXTERIOR CORNERS ####################################
                if (
                    p.neighbor(direction) in perimeter
                    and p.neighbor(direction.clockwise) in perimeter
                    and p.neighbor(direction.clockwise8) in region
                ):
                    yield p
                ############################### INTERIOR CORNERS ####################################
                if (
                    p.neighbor(direction) in region
                    and p.neighbor(direction.clockwise) in region
                ):
                    yield p
