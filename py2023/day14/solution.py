#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Direction, Grid


def shift_grid(grid: Grid, direction: Direction) -> Grid:
    if direction == Direction.UP:
        for p, c in grid.iter():
            if c != "O":
                continue
            while grid.get_direction(p, direction) == ".":
                p = grid.swap_direction(p, direction)
    elif direction == Direction.DOWN:
        for p, c in grid.iter_rev():
            if c != "O":
                continue
            while grid.down(p) == ".":
                p = grid.swap(p, p.down)

    elif direction == Direction.LEFT:
        grid = grid.transpose()
        for p, c in grid.iter():
            if c == "O":
                while grid.up(p) == ".":
                    grid.replace(p.up, "O")
                    grid.replace(p, ".")
                    p = p.up
        grid = grid.transpose()
    elif direction == Direction.RIGHT:
        grid = grid.transpose()
        for p, c in list(grid.iter())[::-1]:
            if c == "O":
                while grid.down(p) == ".":
                    grid.replace(p.down, "O")
                    grid.replace(p, ".")
                    p = p.down
        grid = grid.transpose()
    return grid


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        grid = Grid.from_lines(self.data)
        grid = shift_grid(grid, Direction.UP)
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
        gstring = "".join(["".join(c) for r in grid.rows() for c in r])
        done = False
        cycle_start = 0
        cycle_start_gstring_dir = None

        TARGET = 1000000000 - 1
        for i in range(TARGET):
            if done:
                break
            for d in (Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT):
                grid = shift_grid(grid, d)
                if d == Direction.UP:
                    l_before = len(seen_grids)
                    gstring = "".join(["".join(c) for r in grid.rows() for c in r])
                    seen_grids.add(((gstring, d)))

                    if cycle_start_gstring_dir == (gstring, d):
                        done = True
                        break

                    if l_before == len(seen_grids) and cycle_start == 0:
                        print("cycle_start detected")
                        cycle_start = i
                        cycle_start_gstring_dir = (gstring, d)
                    if cycle_start > 0 and d == cycle_start_gstring_dir[1]:
                        print("adding grid", d)
                        cycle_grids.append(grid)

        print(cycle_start_gstring_dir)
        grid = cycle_grids[(TARGET - cycle_start) % len(cycle_grids)]
        for d in (Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT):
            grid = shift_grid(grid, d)

        ans = 0
        for j, row in enumerate(grid.rows()):
            for i in row:
                if i == "O":
                    ans += grid.h - j
        return ans
