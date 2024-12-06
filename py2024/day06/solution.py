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
        while (pos, dir) not in seen_with_dir:
            seen_with_dir.add((pos, dir))
            match self.grid.get_neighbor(pos, dir):
                case None:
                    return False
                case "#":
                    dir = dir.clockwise
                case _:
                    pos = pos.neighbor(dir)
        return True

    def _part2(self) -> Solution:
        starting_pos = self.grid.find("^")
        pos = starting_pos
        dir = Direction.UP
        seen = set()
        seen_with_dir = set()
        new_obstructions = set()
        allow_obstruction = True
        moved = True
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
                    if (
                        new_pos not in seen
                        and new_pos not in new_obstructions
                        and new_pos != starting_pos
                    ):
                        self.grid.replace(new_pos, "#")
                        if self._check_if_loopable(pos, dir.clockwise, set()):
                            new_obstructions.add(new_pos)
                        self.grid.replace(new_pos, ".")
                    pos = new_pos
