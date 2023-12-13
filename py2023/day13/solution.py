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
            grid = Grid.from_lines(grid_data).transform(lambda x: x == "#")
            for data, factor in ((grid.cols(), 1), (grid.rows(), 100)):
                for mirror_location in range(1, len(data)):
                    sum_of_xors = 0
                    for source_image, reflection in zip(
                        reversed(data[:mirror_location]), data[mirror_location:]
                    ):
                        for a, b in zip(source_image, reflection):
                            sum_of_xors += int(a ^ b)

                    if sum_of_xors == xor_target:
                        ans += mirror_location * factor
                        break

        return ans
