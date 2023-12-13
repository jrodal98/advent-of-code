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
            grid = Grid.from_lines(grid_data)
            grid = grid.transform(lambda x: x == "#")
            columns = [list(col) for col in grid.cols()]
            num_valid = 0
            is_valid = False
            for i in range(len(columns) - 1):
                if is_valid:
                    break
                num_valid = i
                sum_of_xors = 0
                for l, r in zip(list(reversed(columns[: i + 1])), columns[i + 1 :]):
                    for a, b in zip(l, r):
                        sum_of_xors += int(a ^ b)

                is_valid = sum_of_xors == xor_target

            if is_valid:
                ans += num_valid + 1

            columns = [list(col) for col in grid.rows()]
            num_valid = 0
            is_valid = False
            for i in range(len(columns) - 1):
                if is_valid:
                    break
                num_valid = i
                sum_of_xors = 0
                for l, r in zip(list(reversed(columns[: i + 1])), columns[i + 1 :]):
                    for a, b in zip(l, r):
                        sum_of_xors += int(a ^ b)
                is_valid = sum_of_xors == xor_target
            if is_valid:
                ans += (num_valid + 1) * 100

        return ans
