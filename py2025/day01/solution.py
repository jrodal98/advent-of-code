#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        STARTING_POS = 50
        MODULO = 100

        pos = STARTING_POS
        zero_crossings = 0

        for line in self.lines():
            direction = line[0]
            value = int(line[1:])

            raw_pos = pos - value if direction == "L" else pos + value

            if not part1:
                if direction == "L":
                    if pos != 0 and raw_pos <= 0:
                        zero_crossings += 1
                    zero_crossings += abs(int(raw_pos / MODULO))
                else:
                    zero_crossings += int(raw_pos / MODULO)

            pos = raw_pos % MODULO

            if part1 and pos == 0:
                zero_crossings += 1

        return zero_crossings
