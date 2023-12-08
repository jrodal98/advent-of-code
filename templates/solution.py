#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    PART1_EXAMPLE_SOLUTION: Solution | None = None
    PART2_EXAMPLE_SOLUTION: Solution | None = None

    def _part1(self) -> Solution:
        raise NotImplementedError

    def _part2(self) -> Solution:
        raise NotImplementedError
