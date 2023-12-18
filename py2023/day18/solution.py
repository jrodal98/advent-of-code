#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Direction, Point


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return self._compute(use_hex=False)

    def _part2(self) -> Solution:
        return self._compute(use_hex=True)

    def _compute(self, use_hex: bool) -> int:
        last_position = Point(0, 0)
        positions = [last_position]
        num_boundary_points = 0
        for line in self.data.splitlines():
            dir_str, distance_str, hex_str = line.split()
            if use_hex:
                distance = int(hex_str[2:-2], base=16)
                dir_str = hex_str[-2]
            else:
                distance = int(distance_str)
            num_boundary_points += distance

            dir_str = dir_str.translate(str.maketrans("0123", "RDLU"))
            last_position += Direction.from_str(dir_str) * distance
            positions.append(last_position)

        inner_points = Point.num_inner_points(positions, use_lines=True)
        return num_boundary_points + inner_points
