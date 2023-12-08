#!/usr/bin/env python3
# www.jrodal.com

from enum import Enum
import aocd
from urllib3.response import HTTPResponse
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
    response = aocd.post.submit(solution, part=part.value, day=day, year=year)
    if isinstance(response, HTTPResponse):
        if "That's not the right answer." in response.data.decode("utf-8"):
            raise Exception("Wrong answer")
