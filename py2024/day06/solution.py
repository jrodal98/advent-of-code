#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.point import Direction, Point

import functools


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return len(self._helper()[0])

    def _part2(self) -> Solution:
        return sum(self._check_if_loopable(pos, dir) for pos, dir in self._helper()[1])

    def _check_if_loopable(self, pos: Point, dir: Direction) -> bool:
        new_obstacle = pos.neighbor(dir)
        dir = dir.clockwise
        seen = set()
        while (pos, dir) not in seen:
            seen.add((pos, dir))
            neighbor_pos = pos.neighbor(dir)
            match "#" if neighbor_pos == new_obstacle else self.grid.get(neighbor_pos):
                case None:
                    return False
                case "#":
                    dir = dir.clockwise
                case _:
                    pos = pos.neighbor(dir)
        return True

    @functools.cache
    def _helper(self) -> tuple[set[Point], set[tuple[Point, Direction]]]:
        pos = self.grid.find("^")
        dir = Direction.UP
        seen = set()
        check_for_loops = set()
        while True:
            seen.add(pos)
            match self.grid.get_neighbor(pos, dir):
                case None:
                    return seen, check_for_loops
                case "#":
                    dir = dir.clockwise
                case _:
                    new_pos = pos.neighbor(dir)
                    if new_pos not in seen:
                        check_for_loops.add((pos, dir))
                    pos = new_pos
