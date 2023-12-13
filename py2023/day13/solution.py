#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        ans = 0
        for grid_data in self.data.split("\n\n"):
            grid = Grid.from_lines(grid_data)
            valid = True
            split_col = grid.w // 2 + (1 - grid.w % 1)
            for row in grid.rows():
                if not valid:
                    break
                row = list(row)
                for l, r in zip(reversed(row[:split_col]), row[split_col:]):
                    if l != r:
                        valid = False
                        break
            if valid:
                ans += split_col
            valid = True
            grid = grid.transpose()
            split_col = grid.w // 2 + (1 - grid.w % 1)
            for row in grid.rows():
                if not valid:
                    break
                row = list(row)
                for l, r in zip(reversed(row[:split_col]), row[split_col:]):
                    if l != r:
                        valid = False
                        break

            if valid:
                ans += (split_col) * 100
        return ans

    def _part2(self) -> Solution:
        raise NotImplementedError
