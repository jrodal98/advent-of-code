#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return self._compute_solution(0)

    def _part2(self) -> Solution:
        return self._compute_solution(1)

    def _compute_solution(self, xor_target: int) -> int:
        ans = 0
        for grid_data in self.data.split("\n\n"):
            g = Grid.from_lines(grid_data).transform(lambda x: x == "#")
            for grid, factor in ((g, 1), (g.transpose(), 100)):
                columns = [list(col) for col in grid.cols()]
                for col in range(1, len(columns)):
                    sum_of_xors = 0
                    for left_cols, right_cols in zip(
                        list(reversed(columns[:col])), columns[col:]
                    ):
                        for a, b in zip(left_cols, right_cols):
                            sum_of_xors += int(a ^ b)

                    if sum_of_xors == xor_target:
                        ans += col * factor
                        break

        return ans
