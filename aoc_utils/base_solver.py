#!/usr/bin/env python3
# www.jrodal.com

from contextlib import nullcontext
from functools import cache, cached_property
from typing import Callable
import aocd

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


class BaseSolver:
    def __init__(
        self,
        data: str,
        *,
        console: Console | None = None,
        animate: bool = False,
        lag: float = 0,
        step: bool = False,
        is_unit_test: bool = False,
    ) -> None:
        self.data = data.rstrip("\r\n")
        self.console = console or CONSOLE
        self._animation_grid: Grid | None = None
        self._animate: bool = animate
        self._lag_in_seconds: float = lag / 1000
        self._live: Live | None = None
        self._step = step
        self._started_animation = False
        self._is_unit_test = is_unit_test
        self._is_part1: bool = False
        self._is_part2: bool = False

    @cached_property
    def grid(self) -> Grid[str]:
        return Grid.from_lines(self.data)

    def _set_animation_grid(self, grid: Grid | None = None) -> None:
        self._animation_grid = grid or self.grid

    @cache
    def lines(self) -> list[str]:
        return self.data.splitlines()

    @cache
    def sections(self) -> list[str]:
        return self.data.split("\n\n")

    def _update_animation(
        self,
        *,
        point: Point | None = None,
        value: str | None | Callable[[Grid, Point], str | None] = None,
        message: str | None = None,
        points_to_colors: dict[Point | None, str] | None = None,
        values_to_colors: dict[str | None, str] | None = None,
        refresh: bool = True,
    ) -> None:
        points_to_colors = points_to_colors or {point: "green"}
        values_to_colors = values_to_colors or {}
        message = message or str(point)
        if not self._animate or not self._live or not self._animation_grid:
            return

        if refresh and self._step and not self._started_animation:
            self._live.update(str(self._animation_grid), refresh=True)

        if point and value:
            if not isinstance(value, str):
                value = value(self._animation_grid, point) or "x"

            self._animation_grid.replace(point, value)

        if not refresh:
            return

        grid_str = self._animation_grid.colored_str(points_to_colors, values_to_colors)

        if message:
            grid_str = message + "\n\n" + grid_str
        self._live.update(grid_str, refresh=refresh)
        if self._step:
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
            with (
                Live(
                    "",
                    console=self.console,
                    auto_refresh=False,
                )
                if self._animate
                else nullcontext() as live
            ):
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

        if not solution and part is ProblemPart.PART2 and day == 25:
            self.console.print(
                "Not submitting because it's day 25 part2 and a falsy solution was provided"
            )
            return solution, runtime
        response = aocd.post.submit(solution, part=part.value, day=day, year=year)
        if isinstance(response, HTTPResponse):
            if "That's not the right answer." in response.data.decode("utf-8"):
                raise Exception("Wrong answer")

        return solution, runtime

    def part1(self) -> Solution:
        solution = self._solve(part1=True)
        try:
            return int(solution)
        except ValueError:
            return str(solution)

    def part2(self) -> Solution:
        solution = self._solve(part1=False)
        try:
            return int(solution)
        except ValueError:
            return str(solution)

    @classmethod
    def is_not_implemented(cls, part: ProblemPart) -> bool:
        if (
            "raise NotImplementedError"
            not in getsource(cls._solve).strip().splitlines()[-1]
        ):
            return False
        match part:
            case ProblemPart.PART1:
                code = getsource(cls._part1)
            case ProblemPart.PART2:
                code = getsource(cls._part2)
            case _:
                raise ValueError(f"Invalid part {part}")
        return "raise NotImplementedError" in code.strip().splitlines()[-1]

    def _part1(self) -> Solution:
        raise NotImplementedError

    def _part2(self) -> Solution:
        raise NotImplementedError

    def _solve(self, part1: bool) -> Solution:
        if part1:
            return self._part1()
        else:
            return self._part2()
