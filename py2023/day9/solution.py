#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
import numpy as np


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        res = 0
        for line in self.data.splitlines():
            history = np.array([int(i) for i in line.split()])
            res += history[-1]
            while not np.all(history == 0):
                history = np.diff(history)
                res += history[-1]
        return res

    def _part2(self) -> Solution:
        res = 0
        for line in self.data.splitlines():
            history = np.array([int(i) for i in line.split()])
            first_digits = [history[0]]
            while not np.all(history == 0):
                history = np.diff(history)
                first_digits.append(history[0])
            last_digit = 0
            for digit in first_digits[::-1]:
                last_digit = digit - last_digit
            res += last_digit
        return res
