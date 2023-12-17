#!/usr/bin/env python3
# www.jrodal.com

from contextlib import nullcontext
from typing import Callable
import aocd

from abc import ABC, abstractmethod
from enum import Enum
from inspect import getsource
from rich.console import Console
from urllib3.response import HTTPResponse
from aoc_utils.grid import Grid, Point
from aoc_utils.log_runtime import log_runtime, Runtime
from rich.live import Live
from time import sleep

from consts import CONSOLE

Solution = str | int


class ProblemPart(Enum):
    PART1 = "a"
    PART2 = "b"
    UNSPECIFIED = None


class BaseSolver(ABC):
    def __init__(
        self,
        data: str,
        *,
        console: Console | None = None,
        animate: bool = False,
        lag: float = 0,
        manual_step: bool = False,
    ) -> None:
        self.data = data.rstrip("\r\n")
        self.console = console or CONSOLE
        self._animation_grid: Grid | None = None
        self._animate: bool = animate
        self._lag_in_seconds: float = lag / 1000
        self._live: Live | None = None
        self._manual_step = manual_step
        self._started_animation = False

    @property
    def grid(self) -> Grid[str]:
        return Grid.from_lines(self.data)

    def _set_animation_grid(self, grid: Grid | None) -> None:
        self._animation_grid = grid or self.grid

    def _update_animation(
        self,
        *,
        point: Point | None = None,
        value: str | None | Callable[[Grid, Point], str | None] = None,
        message: str | None = None,
        points_to_colors: dict[Point | None, str] | None = None,
    ) -> None:
        points_to_colors = points_to_colors or {point: "green"}
        if not self._animate or not self._live or not self._animation_grid:
            return

        if self._manual_step and not self._started_animation:
            self._live.update(str(self._animation_grid), refresh=True)

        if point:
            value = value or "x"
            if not isinstance(value, str):
                value = value(self._animation_grid, point) or "x"

            self._animation_grid.replace(point, value)

        grid_str = self._animation_grid.colored_str(points_to_colors)

        if message:
            grid_str = message + "\n\n" + grid_str
        self._live.update(grid_str, refresh=True)
        if self._manual_step:
            input()
        elif self._lag_in_seconds:
            sleep(self._lag_in_seconds)
        self._started_animation = True

    def _reset_animation(self) -> None:
        self._live = None
        self._started_animation = False
        self._animation_grid = None

    def solve_and_submit(
        self, part: ProblemPart, *, day: int | None = None, year: int | None = None
    ) -> tuple[Solution, Runtime]:
        with log_runtime(part.name, console=self.console) as runtime:
            with Live(
                "",
                console=self.console,
                auto_refresh=False,
            ) if self._animate else nullcontext() as live:
                self._live = live
                if part is ProblemPart.PART1:
                    solution = self.part1()
                else:
                    solution = self.part2()
                self._reset_animation()

            self.console.print(f"{part.name}: {solution}")

        if self._animate:
            self.console.print("Not submitting because animation is enabled")
            return solution, runtime

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
