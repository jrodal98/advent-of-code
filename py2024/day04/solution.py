#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.point import Direction


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return sum(
            all(
                expected == actual
                for expected, actual in zip(
                    "MAS",
                    self.grid.walk_directions(point, [direction] * 3, default="."),
                )
            )
            for point, _ in self.grid.iter(qualify="X")
            for direction in Direction
        )

    def _part2(self) -> Solution:
        ans = 0
        for point, c in self.grid.iter():
            if c != "A":
                continue

            upper_left = self.grid.get(point.upper_left, ".")
            bottom_right = self.grid.get(point.bottom_right, ".")

            if not (
                upper_left == "S"
                and bottom_right == "M"
                or upper_left == "M"
                and bottom_right == "S"
            ):
                continue

            upper_right = self.grid.get(point.upper_right, ".")
            bottom_left = self.grid.get(point.bottom_left, ".")

            if not (
                upper_right == "S"
                and bottom_left == "M"
                or upper_right == "M"
                and bottom_left == "S"
            ):
                continue

            ans += 1

        return ans
