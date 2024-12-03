#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
import re


class Solver(BaseSolver):
    _MULTIPLY_PATTERN: re.Pattern = re.compile(r"mul\((\d+),(\d+)\)")

    def _multiply_some_numbers(self, input_string: str) -> int:
        return sum(
            int(a) * int(b) for a, b in self._MULTIPLY_PATTERN.findall(input_string)
        )

    def _part1(self) -> Solution:
        return self._multiply_some_numbers(self.data)

    def _part2(self) -> Solution:
        ans = 0
        enabled = True
        for token in re.split(r"(do\(\)|don't\(\))", self.data):
            if token == "do()":
                enabled = True
            elif token == "don't()":
                enabled = False
            elif enabled:
                ans += self._multiply_some_numbers(token)
        return ans
