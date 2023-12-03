#!/usr/bin/env python3
# www.jrodal.com

from enum import Enum
import aocd
from aoc_utils.base_solver import Solution


class ProblemPart(Enum):
    PART1 = "a"
    PART2 = "b"
    UNSPECIFIED = None


def submit(
    solution: Solution,
    part: ProblemPart = ProblemPart.UNSPECIFIED,
    day: int | None = None,
    year: int | None = None,
) -> None:
    aocd.post.submit(solution, part=part.value, day=day, year=year)
