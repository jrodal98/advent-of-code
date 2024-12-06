#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid
from aoc_utils.point import Direction, Point

from dataclasses import dataclass

from mpire.pool import WorkerPool


class Solver(BaseSolver):
    @dataclass
    class Result:
        seen: set[Point]
        possible_obstacles: set[tuple[Point, Direction]]
        cycle: bool

    def _part1(self) -> Solution:
        return len(self.walk(self.grid, self.grid.find("^"), Direction.UP).seen)

    def _part2(self) -> Solution:
        with WorkerPool(shared_objects=self.grid) as pool:
            return sum(
                r.cycle
                for r in pool.map(
                    self.walk,
                    [
                        (pos, dir.clockwise, pos.neighbor(dir))
                        for pos, dir in self.walk(
                            self.grid, self.grid.find("^"), Direction.UP
                        ).possible_obstacles
                    ],
                    progress_bar=not self._is_unit_test,
                )
            )

    @classmethod
    def walk(
        cls, grid: Grid, pos: Point, dir: Direction, new_obstacle: Point | None = None
    ) -> "Solver.Result":
        seen = set()
        seen_with_dir = set()
        possible_obstacles = set()
        while (pos, dir) not in seen_with_dir:
            seen.add(pos)
            seen_with_dir.add((pos, dir))
            neighbor_pos = pos.neighbor(dir)
            match "#" if neighbor_pos == new_obstacle else grid.get(neighbor_pos):
                case None:
                    return cls.Result(seen, possible_obstacles, False)
                case "#":
                    dir = dir.clockwise
                case _:
                    new_pos = pos.neighbor(dir)
                    if new_pos not in seen:
                        possible_obstacles.add((pos, dir))
                    pos = new_pos
        return cls.Result(seen, possible_obstacles, True)
