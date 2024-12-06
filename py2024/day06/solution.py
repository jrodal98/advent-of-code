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

    def _check_if_loopable(
        self, pos: Point, dir: Direction, seen_with_dir: set[tuple[Point, Direction]]
    ) -> bool:
        if (pos, dir) in seen_with_dir:
            return True
        if self.grid.get_neighbor(pos, dir) is None:
            return False
        seen_with_dir.add((pos, dir))
        if self.grid.get_neighbor(pos, dir, "#") == "#":
            dir = dir.clockwise

        return self._check_if_loopable(pos.neighbor(dir), dir, seen_with_dir)

    def _part2(self) -> Solution:
        pos = self.grid.find("^")
        dir = Direction.UP
        seen = set()
        seen_with_dir = set()
        new_obstructions = set()
        while True:
            seen.add(pos)
            seen_with_dir.add((pos, dir))
            match self.grid.get_neighbor(pos, dir):
                case None:
                    return len(new_obstructions)
                case "#":
                    dir = dir.clockwise
                case _:
                    new_pos = pos.neighbor(dir)
                    self.grid.replace(new_pos, "#")
                    if self._check_if_loopable(
                        pos, dir.clockwise, seen_with_dir.copy()
                    ):
                        new_obstructions.add(pos.neighbor(dir))
                    self.grid.replace(new_pos, ".")
                    pos = new_pos
