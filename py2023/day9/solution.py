#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
import numpy as np


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        res = 0
        for line in self.data.splitlines():
            history = np.array([int(i) for i in line.split()])
            differences = np.diff(history)
            all_zero = np.all(differences == 0)
            last_digits = [history[-1]]
            while not all_zero:
                history = differences
                differences = np.diff(history)
                all_zero = np.all(differences == 0)
                last_digits.append(history[-1])
            last_digits.append(0)
            cumsum = np.cumsum(sorted(last_digits))
            res += cumsum[-1]
        return res

    def _part2(self) -> Solution:
        res = 0
        for line in self.data.splitlines():
            history = np.array([int(i) for i in line.split()])
            differences = np.diff(history)
            all_zero = np.all(differences == 0)
            first_digits = [history[0]]
            while not all_zero:
                history = differences
                differences = np.diff(history)
                all_zero = np.all(differences == 0)
                first_digits.append(history[0])

            last_digit = 0
            for digit in first_digits[::-1]:
                last_digit = digit - last_digit
            res += last_digit
        return res
