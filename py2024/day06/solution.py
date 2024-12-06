#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.point import Direction, Point


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        pos = self.grid.find("^")
        dir = Direction.UP
        seen = set()
        while True:
            seen.add(pos)
            match self.grid.get_neighbor(pos, dir):
                case None:
                    return len(seen)
                case "#":
                    dir = dir.clockwise
                case _:
                    pos = pos.neighbor(dir)

    def _check_if_loopable(self, pos: Point, dir: Direction) -> bool:
        new_obstacle = pos.neighbor(dir)
        dir = dir.clockwise
        seen = set()
        while (pos, dir) not in seen:
            seen.add((pos, dir))
            if pos.neighbor(dir) == new_obstacle:
                v = "#"
            else:
                v = self.grid.get_neighbor(pos, dir)
            match v:
                case None:
                    return False
                case "#":
                    dir = dir.clockwise
                case _:
                    pos = pos.neighbor(dir)
        return True

    def _part2(self) -> Solution:
        pos = self.grid.find("^")
        dir = Direction.UP
        seen = set()
        check_for_loops = set()
        ans = 0
        while True:
            seen.add(pos)
            match self.grid.get_neighbor(pos, dir):
                case None:
                    return sum(
                        self._check_if_loopable(pos, dir)
                        for pos, dir in check_for_loops
                    )
                case "#":
                    dir = dir.clockwise
                case _:
                    new_pos = pos.neighbor(dir)
                    if new_pos not in seen:
                        check_for_loops.add((pos, dir))
                    pos = new_pos
