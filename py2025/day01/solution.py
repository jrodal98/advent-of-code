#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        pos = 50
        modulo = 100
        num_zeros = 0
        lines = self.lines()
        for line in lines:
            if line[0] == "L":
                raw_pos = pos - int(line[1:])
                if not part1:
                    if pos != 0 and raw_pos <= 0:
                        num_zeros += 1
                    num_zeros += abs(int(raw_pos / modulo))
                pos = raw_pos % modulo
            else:
                raw_pos = pos + int(line[1:])
                if not part1:
                    num_zeros += int(raw_pos / modulo)
                pos = raw_pos % modulo
            if part1 and pos == 0:
                num_zeros += 1
        return num_zeros
