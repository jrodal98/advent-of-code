#!/usr/bin/env python3
# www.jrodal.com

import aocd

from abc import ABC, abstractmethod
from enum import Enum
from inspect import getsource
from rich.console import Console
from urllib3.response import HTTPResponse
from aoc_utils.log_runtime import log_runtime, Runtime

from consts import CONSOLE

Solution = str | int


class ProblemPart(Enum):
    PART1 = "a"
    PART2 = "b"
    UNSPECIFIED = None


class BaseSolver(ABC):
    def __init__(self, data: str, *, console: Console | None = None) -> None:
        self.data = data.rstrip("\r\n")
        self.console = console or CONSOLE

    def solve_and_submit(
        self, part: ProblemPart, *, day: int | None = None, year: int | None = None
    ) -> tuple[Solution, Runtime]:
        with log_runtime(part.name, console=self.console) as runtime:
            if part is ProblemPart.PART1:
                solution = self.part1()
            else:
                solution = self.part2()

            self.console.print(f"{part.name}: {solution}")

        response = aocd.post.submit(solution, part=part.value, day=day, year=year)
        if isinstance(response, HTTPResponse):
            if "That's not the right answer." in response.data.decode("utf-8"):
                raise Exception("Wrong answer")

        return solution, runtime

    def part1(self) -> Solution:
        solution = self._part1()
        try:
            return int(solution)
        except ValueError:
            return str(solution)

    def part2(self) -> Solution:
        solution = self._part2()
        try:
            return int(solution)
        except ValueError:
            return str(solution)

    @classmethod
    def is_not_implemented(cls, part: ProblemPart) -> bool:
        match part:
            case ProblemPart.PART1:
                code = getsource(cls._part1)
            case ProblemPart.PART2:
                code = getsource(cls._part2)
            case _:
                raise ValueError(f"Invalid part {part}")
        return "raise NotImplementedError" in code.strip().splitlines()[-1]

    @abstractmethod
    def _part1(self) -> Solution:
        ...

    @abstractmethod
    def _part2(self) -> Solution:
        ...
