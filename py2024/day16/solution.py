#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid
from aoc_utils.point import Direction, Point

MAX_COST = 10000000000000000000000000000000000000000000

import sys

sys.setrecursionlimit(100000)


def _min_cost(
    grid: Grid,
    direction: Direction,
    start: Point,
    end: Point,
    seen: dict[tuple[Point, Direction], tuple[int, int]],
    cost: int = 0,
) -> int:
    if start == end:
        return cost
    min_cost = MAX_COST
    key = (start, direction)
    if key in seen:
        seen_acc_cost, min_cost = seen[key]
        if cost > seen_acc_cost:
            return min_cost

    seen[key] = (cost, min_cost)
    if grid.at(neighbor := start.neighbor(direction)) != "#":
        min_cost = min(
            min_cost, _min_cost(grid, direction, neighbor, end, seen, cost + 1)
        )

    for d in [
        direction.counter_clockwise,
        direction.clockwise,
    ]:
        if min_cost > cost + 1000:
            min_cost = min(min_cost, _min_cost(grid, d, start, end, seen, cost + 1000))

    seen[key] = (cost, min_cost)
    return min_cost


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        start_node = self.grid.find("S")
        end_node = self.grid.find("E")
        return _min_cost(self.grid, Direction.RIGHT, start_node, end_node, {}, 0)
