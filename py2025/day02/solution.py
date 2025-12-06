#!/usr/bin/env python3
# www.jrodal.com

import math
import textwrap
from functools import cache
from aoc_utils.base_solver import BaseSolver, Solution


@cache
def _get_divisors(n: int) -> list[int]:
    divisors = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)
    divisors.remove(n)
    return sorted(divisors, reverse=True)


def _part1_id_val(val: int) -> int:
    val_str = str(val)
    if len(val_str) % 2 == 1:
        return 0
    elif val_str[: len(val_str) // 2] == val_str[len(val_str) // 2 :]:
        return val
    else:
        return 0


def _part2_id_val(val: int) -> int:
    val_str = str(val)
    divisors = _get_divisors(len(val_str))
    for d in divisors:
        chunks = textwrap.wrap(val_str, d)
        if len(set(chunks)) == 1:
            return val
    return 0


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        ranges = [tuple(map(int, r.split("-"))) for r in self.data.split(",")]
        val_func = _part1_id_val if part1 else _part2_id_val
        return sum(val_func(i) for x, y in ranges for i in range(x, y + 1))
