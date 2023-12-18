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
        total_distance = 0
        for line in self.data.splitlines():
            dir_str, distance_str, hex_str = line.split()
            if use_hex:
                distance = int(hex_str[2:-2], base=16)
                dir_str = hex_str[-2]
            else:
                distance = int(distance_str)
            total_distance += distance

            match dir_str:
                case "R" | "0":
                    last_position += Direction.RIGHT * distance
                case "L" | "2":
                    last_position += Direction.LEFT * distance
                case "U" | "3":
                    last_position += Direction.UP * distance
                case "D" | "1":
                    last_position += Direction.DOWN * distance
                case _:
                    assert False
            positions.append(last_position)

        shoelace = positions + [positions[0]]

        area = 0
        for p1, p2 in zip(shoelace, shoelace[1:]):
            area += (p1.x * p2.y) - (p1.y * p2.x)
        return int(abs(area) / 2 + total_distance / 2 + 1)
