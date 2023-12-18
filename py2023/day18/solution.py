#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Point


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        last_position = Point(0, 0)
        positions = [last_position]
        total_distance = 0
        for line in self.data.splitlines():
            d, n, _ = line.split()
            n = int(n)
            total_distance += n
            match d:
                case "R":
                    last_position = last_position + Point(n, 0)
                case "L":
                    last_position = last_position - Point(n, 0)
                case "U":
                    last_position = last_position + Point(0, n)
                case "D":
                    last_position = last_position - Point(0, n)
                case _:
                    assert False
            positions.append(last_position)

        shoelace = positions + [positions[0]]

        area = 0
        for a, b in zip(shoelace, shoelace[1:]):
            area += (a.x * b.y) - (a.y * b.x)
        return int(abs(area) / 2 + total_distance / 2 + 1)

    def _part2(self) -> Solution:
        last_position = Point(0, 0)
        positions = [last_position]
        total_distance = 0
        for line in self.data.splitlines():
            _, _, hex_str = line.split()
            distance_encoded = hex_str[2:-2]
            d = hex_str[-2]
            n = int(distance_encoded, base=16)
            total_distance += n
            match d:
                case "0":
                    last_position = last_position + Point(n, 0)
                case "2":
                    last_position = last_position - Point(n, 0)
                case "3":
                    last_position = last_position + Point(0, n)
                case "1":
                    last_position = last_position - Point(0, n)
                case _:
                    assert False
            positions.append(last_position)

        shoelace = positions + [positions[0]]

        area = 0
        for a, b in zip(shoelace, shoelace[1:]):
            area += (a.x * b.y) - (a.y * b.x)
        return int(abs(area) / 2 + total_distance / 2 + 1)
