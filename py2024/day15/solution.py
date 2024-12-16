#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.point import Direction, Point
from aoc_utils.grid import Grid


class Solver(BaseSolver):
    @classmethod
    def _push(cls, grid: Grid, pos: Point, direction: Direction) -> bool:
        next_pos = pos + direction

        check = []
        match grid[next_pos]:
            case "#":
                return False
            case "[":
                check = [next_pos + Direction.RIGHT, next_pos]
            case "]":
                check = [next_pos + Direction.LEFT, next_pos]
            case "O":
                check = [next_pos]
        if not all((cls._push(grid, p, direction) for p in check)):
            return False

        grid.swap(pos, next_pos)
        return True

    def _solve(self, part1: bool) -> Solution:
        warehouse_map, motions = self.sections()
        if not part1:
            warehouse_map = (
                warehouse_map.replace("#", "##")
                .replace(".", "..")
                .replace("O", "[]")
                .replace("@", "@.")
            )
        grid = Grid.from_lines(warehouse_map)
        robot = grid.find("@")
        for direction in (
            Direction.from_str(m) for line in motions.split() for m in line
        ):
            old_grid = grid.copy(deep=False)
            if self._push(grid, robot, direction):
                robot += direction
            else:
                grid = old_grid

        return sum(
            box.x + 100 * box.y for box, _ in grid.iter(include="O" if part1 else "[")
        )
