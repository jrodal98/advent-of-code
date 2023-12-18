#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Direction, Grid, Point


def can_escape(grid: Grid, current_position: Point, escaped: dict[Point, bool]) -> bool:
    if current_position in escaped:
        return escaped[current_position]

    escaped[current_position] = False

    v = grid.at(current_position)
    if v == "#":
        return False

    neighbors = list(grid.neighbors_with_direction(current_position))
    if len(neighbors) < 4:
        escaped[current_position] = True
        return True
    for _, dir in neighbors:
        neighbor_escaped = can_escape(grid, current_position.neighbor(dir), escaped)
        if neighbor_escaped:
            escaped[current_position] = True
            return True

    return False


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

        dummy_points = ["." for _ in range(h * w)]
        grid = Grid(dummy_points, w=w, h=h)
        for p in adjusted_positions:
            grid.replace(p, "#")

        escaped = {}
        for p, _ in grid.iter():
            can_escape(grid, p, escaped)

        for p, esc in escaped.items():
            if not esc:
                grid.replace(p, "#")

        grid.display()

        return len(list(grid.findall("#")))

    def _part2(self) -> Solution:
        raise NotImplementedError
