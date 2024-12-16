#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid
from aoc_utils.point import Direction, Point
from functools import cache

MAX_COST = 10000000000000000000000000000000000000000000


def _min_cost(
    grid: Grid,
    direction: Direction,
    start: Point,
    seen: dict[tuple[Point, Direction], int],
) -> int:
    key = (start, direction)
    if key in seen:
        return seen[key]

    min_cost = MAX_COST
    seen[key] = min_cost
    for d, cost_factor in [
        # step
        (direction, 1),
        # rotate, then step
        (direction.clockwise, 1001),
        # rotate, then step
        (direction.counter_clockwise, 1001),
        # # rotate twice, then step - this should never make sense to do
        (direction.clockwise.clockwise, 2001),
    ]:
        if min_cost < cost_factor:
            break
        neighbor = start.neighbor(d)
        if grid.at(neighbor) != "#":
            min_cost = min(min_cost, cost_factor + _min_cost(grid, d, neighbor, seen))

    seen[key] = min_cost
    return min_cost


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        start_node = self.grid.find("S")
        end_node = self.grid.find("E")
        costs = {(end_node, d): 0 for d in Direction.dir4()}
        return _min_cost(
            self.grid,
            Direction.RIGHT,
            start_node,
            costs,
        )
