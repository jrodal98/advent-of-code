#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        ans = 0
        for grid_data in self.data.split("\n\n"):
            grid = Grid.from_lines(grid_data)
            columns = [list(col) for col in grid.cols()]
            num_valid = 0
            is_valid = False
            for i in range(len(columns)):
                if is_valid:
                    break
                num_valid = i
                for l, r in zip(list(reversed(columns[: i + 1])), columns[i + 1 :]):
                    is_valid = True
                    if l != r:
                        is_valid = False
                        break
            if is_valid:
                ans += num_valid + 1

            columns = [list(col) for col in grid.rows()]
            num_valid = 0
            is_valid = False
            for i in range(len(columns)):
                if is_valid:
                    break
                num_valid = i
                for l, r in zip(list(reversed(columns[: i + 1])), columns[i + 1 :]):
                    is_valid = True
                    if l != r:
                        is_valid = False
                        break
            if is_valid:
                ans += (num_valid + 1) * 100

        return ans

    def _part2(self) -> Solution:
        raise NotImplementedError
