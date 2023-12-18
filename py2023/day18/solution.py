#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Direction, Grid, Point


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        last_position = Point(0, 0)
        positions = [last_position]
        for line in self.data.splitlines():
            d, n, _ = line.split()
            n = int(n)
            match d:
                case "R":
                    direction = Direction.RIGHT
                case "L":
                    direction = Direction.LEFT
                case "U":
                    direction = Direction.UP
                case "D":
                    direction = Direction.DOWN
                case _:
                    assert False
            for _ in range(n):
                last_position = last_position.neighbor(direction)
                positions.append(last_position)

        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0
        for p in positions:
            min_x = min(min_x, p.x)
            min_y = min(min_y, p.y)
            max_x = max(max_x, p.x)
            max_y = max(max_y, p.y)

        h = max_y - min_y + 1
        w = max_x - min_x + 1

        adjusted_positions = []
        for p in positions:
            adjusted_positions.append(p.translate(min_x, min_y))

        print(adjusted_positions)
        dummy_points = ["." for _ in range(h * w)]
        grid = Grid(dummy_points, w=w, h=h)
        for p in adjusted_positions:
            grid.replace(p, "#")

        grid.display()

        return 0

    def _part2(self) -> Solution:
        raise NotImplementedError
