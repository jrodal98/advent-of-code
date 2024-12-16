#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.point import Direction, Point
from aoc_utils.grid import Grid


class Solver(BaseSolver):
    @classmethod
    def _push(cls, g: Grid, p: Point, d: Direction) -> bool:
        p += d
        if all(
            [
                g[p] != "["
                or cls._push(g, p + Direction.RIGHT, d)
                and cls._push(g, p, d),
                g[p] != "]"
                or cls._push(g, p + Direction.LEFT, d)
                and cls._push(g, p, d),
                g[p] != "O" or cls._push(g, p, d),
                g[p] != "#",
            ]
        ):
            g.swap(p, p - d)
            return True
        return False

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
            match grid[robot + direction]:
                case "#":
                    continue
                case ".":
                    robot = grid.swap(robot, direction)
                case _:
                    old_grid = grid.copy(deep=False)
                    if self._push(grid, robot, direction):
                        robot += direction
                    else:
                        grid = old_grid

        return sum(
            box.x + 100 * box.y for box, _ in grid.iter(include="O" if part1 else "[")
        )
