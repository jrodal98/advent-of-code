#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Direction, Grid


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        grid = Grid.from_lines(self.data)
        grid = self._shift_grid(grid, Direction.UP)
        ans = 0
        for j, row in enumerate(grid.rows()):
            for i in row:
                if i == "O":
                    ans += grid.h - j
        return ans

    def _part2(self) -> Solution:
        grid = Grid.from_lines(self.data)
        seen_grids = set()
        cycle_grids = []
        cycle_start = 0

        TARGET = 1000000000 - 1
        for i in range(TARGET):
            for d in (Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT):
                grid = self._shift_grid(grid, d)
                if d == Direction.UP:
                    if grid in seen_grids:
                        if cycle_grids:
                            grid = cycle_grids[
                                (TARGET - cycle_start) % len(cycle_grids)
                            ]
                            for d in (
                                Direction.UP,
                                Direction.LEFT,
                                Direction.DOWN,
                                Direction.RIGHT,
                            ):
                                grid = self._shift_grid(grid, d)

                            return self._score_grid(grid)
                        else:
                            print("cycle_start detected")
                            cycle_start = i
                            seen_grids = set()

                    seen_grids.add(grid)
                    if cycle_start > 0:
                        print("adding grid", d)
                        cycle_grids.append(grid)

        grid = cycle_grids[(TARGET - cycle_start) % len(cycle_grids)]
        for d in (Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT):
            grid = self._shift_grid(grid, d)

        return self._score_grid(grid)

    def _score_grid(self, grid: Grid) -> int:
        ans = 0
        for j, row in enumerate(grid.rows()):
            for i in row:
                if i == "O":
                    ans += grid.h - j
        return ans

    def _shift_grid(self, grid: Grid, direction: Direction) -> Grid:
        transposed = direction in (Direction.LEFT, Direction.RIGHT)
        direction = {Direction.LEFT: Direction.UP, Direction.RIGHT: Direction.DOWN}.get(
            direction, direction
        )
        reverse = direction is Direction.DOWN

        if transposed:
            grid = grid.transpose()

        for p, c in grid.iter(reverse):
            if c != "O":
                continue
            while grid.get_direction(p, direction) == ".":
                p = grid.swap_direction(p, direction)

        return grid.transpose() if transposed else grid
