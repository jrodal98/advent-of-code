#!/usr/bin/env python3
# www.jrodal.com

import re

from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    PART1_EXAMPLE_SOLUTION: Solution | None = 142
    PART2_EXAMPLE_SOLUTION: Solution | None = 281

    @classmethod
    def _do_part1(cls, s: str) -> Solution:
        res = 0
        for line in s.split():
            digits = []
            for c in line:
                try:
                    int(c)
                    digits.append(c)
                except Exception:
                    pass
            res += int(digits[0] + digits[-1])
        return res

    def part1(self) -> Solution:
        return self._do_part1(self.data)

    def part2(self) -> Solution:
        s = self.data
        rep = {
            "one": "1e",
            "two": "2o",
            "three": "3e",
            "four": "4r",
            "five": "5e",
            "six": "6x",
            "seven": "7n",
            "eight": "8t",
            "nine": "9e",
        }

        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        s = pattern.sub(lambda m: rep[re.escape(m.group(0))], s)
        s = pattern.sub(lambda m: rep[re.escape(m.group(0))], s)
        return self._do_part1(s)
