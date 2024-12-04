#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        ans = 0
        for point, c in self.grid.iter():
            right = (
                c
                + self.grid.get(point.right, ".")
                + self.grid.get(point.right.right, ".")
                + self.grid.get(point.right.right.right, ".")
            )
            left = (
                c
                + self.grid.get(point.left, ".")
                + self.grid.get(point.left.left, ".")
                + self.grid.get(point.left.left.left, ".")
            )
            up = (
                c
                + self.grid.get(point.up, ".")
                + self.grid.get(point.up.up, ".")
                + self.grid.get(point.up.up.up, ".")
            )
            down = (
                c
                + self.grid.get(point.down, ".")
                + self.grid.get(point.down.down, ".")
                + self.grid.get(point.down.down.down, ".")
            )
            upper_right = (
                c
                + self.grid.get(point.upper_right, ".")
                + self.grid.get(point.upper_right.upper_right, ".")
                + self.grid.get(point.upper_right.upper_right.upper_right, ".")
            )
            upper_left = (
                c
                + self.grid.get(point.upper_left, ".")
                + self.grid.get(point.upper_left.upper_left, ".")
                + self.grid.get(point.upper_left.upper_left.upper_left, ".")
            )
            bottom_right = (
                c
                + self.grid.get(point.bottom_right, ".")
                + self.grid.get(point.bottom_right.bottom_right, ".")
                + self.grid.get(point.bottom_right.bottom_right.bottom_right, ".")
            )
            bottom_left = (
                c
                + self.grid.get(point.bottom_left, ".")
                + self.grid.get(point.bottom_left.bottom_left, ".")
                + self.grid.get(point.bottom_left.bottom_left.bottom_left, ".")
            )

            if up in ("XMAS", "SAMX"):
                ans += 1

            if down in ("XMAS", "SAMX"):
                ans += 1

            if right in ("XMAS", "SAMX"):
                ans += 1

            if left in ("XMAS", "SAMX"):
                ans += 1

            if upper_right in ("XMAS", "SAMX"):
                ans += 1

            if upper_left in ("XMAS", "SAMX"):
                ans += 1

            if bottom_right in ("XMAS", "SAMX"):
                ans += 1

            if bottom_left in ("XMAS", "SAMX"):
                ans += 1

        return ans // 2

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
