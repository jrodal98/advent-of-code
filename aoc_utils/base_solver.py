#!/usr/bin/env python3
# www.jrodal.com

from abc import ABC, abstractmethod

Solution = str | int


class BaseSolver(ABC):
    PART1_EXAMPLE_SOLUTION: Solution | None = None
    PART2_EXAMPLE_SOLUTION: Solution | None = None

    def __init__(self, data: str) -> None:
        self.data = data

    @abstractmethod
    def part1(self) -> Solution:
        ...

    @abstractmethod
    def part2(self) -> Solution:
        ...
