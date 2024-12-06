#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid
from aoc_utils.point import Direction, Point

import functools


def walk(
    grid: Grid, pos: Point, dir: Direction, new_obstacle: Point | None = None
) -> tuple[set[Point], set[tuple[Point, Direction]]] | None:
    seen = set()
    seen_with_dir = set()
    check_for_loops = set()
    while (pos, dir) not in seen_with_dir:
        seen.add(pos)
        seen_with_dir.add((pos, dir))
        neighbor_pos = pos.neighbor(dir)
        match "#" if neighbor_pos == new_obstacle else grid.get(neighbor_pos):
            case None:
                return seen, check_for_loops
            case "#":
                dir = dir.clockwise
            case _:
                new_pos = pos.neighbor(dir)
                if new_pos not in seen:
                    check_for_loops.add((pos, dir))
                pos = new_pos
    return None


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return len(self._helper()[0])

    def _part2(self) -> Solution:
        return sum(
            not walk(self.grid, pos, dir.clockwise, new_obstacle=pos.neighbor(dir))
            for pos, dir in self._helper()[1]
        )

    @functools.cache
    def _helper(self) -> tuple[set[Point], set[tuple[Point, Direction]]]:
        pos = self.grid.find("^")
        dir = Direction.UP
        return walk(self.grid, pos, dir) or (set(), set())
