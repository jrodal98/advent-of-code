#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        key_col_counts = []
        lock_col_counts = []
        for grid in (Grid.from_lines(lines) for lines in self.sections()):
            col_counts = [sum(c == "#" for c in col) for col in grid.iter_cols()]
            if grid[(0, 0)] == ".":
                key_col_counts.append(col_counts)
            else:
                lock_col_counts.append(col_counts)

        return sum(
            all(
                key_col + lock_col <= 7
                for key_col, lock_col in zip(key_cols, lock_cols)
            )
            for key_cols in key_col_counts
            for lock_cols in lock_col_counts
        )

    def _part2(self) -> Solution:
        return 0
