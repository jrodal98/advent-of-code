#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.point import Direction, Point
from aoc_utils.grid import Grid


class Solver(BaseSolver):
    @classmethod
    def _get_next_pos(cls, grid, cur_pos: Point, direction: Direction) -> Point:
        next_pos = cur_pos + direction
        next_val = grid.get(next_pos, "#")
        if next_val == "#":
            return cur_pos

        if next_val == "." or cls._get_next_pos(grid, next_pos, direction) != next_pos:
            return grid.swap(cur_pos, next_pos)
        else:
            return cur_pos

    def _solve(self, part1: bool) -> Solution:
        warehouse_map, motions = self.sections()
        grid = Grid.from_lines(warehouse_map.strip())
        robot = grid.find("@")
        for direction in (
            Direction.from_str(m) for line in motions.split() for m in line
        ):
            robot = self._get_next_pos(grid, robot, direction)

        return sum(box_pos.x + 100 * box_pos.y for box_pos, _ in grid.iter(include="O"))
