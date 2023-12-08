#!/usr/bin/env python3
# www.jrodal.com

from abc import ABC, abstractmethod
from rich.console import Console

from aoc_utils.log_runtime import log_runtime
from consts import CONSOLE

Solution = str | int


class BaseSolver(ABC):
    PART1_EXAMPLE_SOLUTION: Solution | None = None
    PART2_EXAMPLE_SOLUTION: Solution | None = None

    def __init__(self, data: str, *, console: Console | None = None) -> None:
        self.data = data
        self.console = console or CONSOLE

    def part1(self) -> Solution:
        with log_runtime("Part 1", console=self.console):
            return self._part1()

    def part2(self) -> Solution:
        with log_runtime("Part 2", console=self.console):
            return self._part2()

    @abstractmethod
    def _part1(self) -> Solution:
        ...

    @abstractmethod
    def _part2(self) -> Solution:
        ...
