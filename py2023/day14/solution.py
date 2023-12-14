#!/usr/bin/env python3
# www.jrodal.com

from functools import cache
from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid


@cache
def shift_grid(grid: Grid, direction: str) -> Grid:
    if direction == "U":
        for _ in range(grid.h):
            for p, c in grid.iter():
                if c == "O" and grid.up(p) == ".":
                    grid.replace(p.up, "O")
                    grid.replace(p, ".")
    elif direction == "D":
        for _ in range(grid.h):
            for p, c in list(grid.iter())[::-1]:
                if c == "O" and grid.down(p) == ".":
                    grid.replace(p.down, "O")
                    grid.replace(p, ".")
    elif direction == "L":
        # grid.display()
        grid = grid.transpose()
        for _ in range(grid.h):
            for p, c in grid.iter():
                if c == "O" and grid.up(p) == ".":
                    grid.replace(p.up, "O")
                    grid.replace(p, ".")
        grid = grid.transpose()
        # grid.display()
        # assert False
    elif direction == "R":
        grid = grid.transpose()
        for _ in range(grid.h):
            for p, c in list(grid.iter())[::-1]:
                if c == "O" and grid.down(p) == ".":
                    grid.replace(p.down, "O")
                    grid.replace(p, ".")
        grid = grid.transpose()
    return grid


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        grid = Grid.from_lines(self.data)
        grid = shift_grid(grid, "U")
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
            for d in "ULDR":
                if i > 1000 and d == "U":
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
                grid = shift_grid(grid, d)

        print(cycle_start_gstring_dir)
        grid = cycle_grids[(TARGET - cycle_start) % len(cycle_grids)]
        for d in "ULDR":
            grid = shift_grid(grid, d)
        # grid.display()
        # for d in "ULDR":
        #     grid = shift_grid(grid, d)

        ans = 0
        for j, row in enumerate(grid.rows()):
            for i in row:
                if i == "O":
                    ans += grid.h - j
        return ans
