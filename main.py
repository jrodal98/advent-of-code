#!/usr/bin/env python3
# www.jrodal.com

import importlib
import os
import shutil
import click
import aocd

from enum import Enum

from rich.traceback import install
from aoc_utils.log_runtime import log_runtime, print_runtime_table

from aoc_utils.rich_test_runner import RichTestRunner
from aoc_utils.solution_submitter import ProblemPart, submit
from aoc_utils.walk_directory import walk_directory

from consts import YEAR, DAY, CONSOLE


def gen_solution_dir(day: int, year: int) -> str:
    return os.path.join(f"py{year}", f"day{day}")


class Task(Enum):
    RUN_PART1_TESTS = "Running Part1 tests"
    SOLVE_PART1 = "Solving Part1"
    RUN_PART2_TESTS = "Running Part2 tests"
    SOLVE_PART2 = "Solving Part2"


@click.group()
def cli():
    pass


@cli.command()
@click.option("--year", default=YEAR, type=int, help="Year to solve")
@click.option("--day", default=DAY, type=int, help="Day to solve")
def init(
    day: int,
    year: int,
):
    CONSOLE.log("AOC Solver!", log_locals=True)
    p = gen_solution_dir(day, year)
    shutil.copytree("templates", p)
    walk_directory(p, CONSOLE)


@cli.command()
@click.option(
    "--log-locals",
    is_flag=True,
    show_default=True,
    default=False,
    help="Log local variables in traceback",
)
@click.option(
    "--skip-part2",
    is_flag=True,
    show_default=True,
    default=False,
    help="Don't run part2",
)
@click.option(
    "--skip-part1",
    is_flag=True,
    show_default=True,
    default=False,
    help="Don't run part1",
)
@click.option(
    "--skip-tests", is_flag=True, show_default=True, default=False, help="Year to solve"
)
@click.option("--year", default=YEAR, type=int, help="Year to solve")
@click.option("--day", default=DAY, type=int, help="Day to solve")
def solve(
    day: int,
    year: int,
    skip_tests: bool,
    skip_part1: bool,
    skip_part2: bool,
    log_locals: bool,
):
    day = day
    year = year

    install(suppress=[click], show_locals=log_locals)

    module_path = gen_solution_dir(day, year).replace("/", ".")

    tests_module = importlib.import_module(f"{module_path}.tests")
    solution_module = importlib.import_module(f"{module_path}.solution")

    part1_runtime_obj = None
    part2_runtime_obj = None

    if not skip_part1:
        if not skip_tests:
            RichTestRunner(tb_locals=log_locals).make_suite_and_run(
                tests_module.PartOneUnitTests
            )
        with log_runtime("Part 1", console=CONSOLE) as runtime:
            solution = solution_module.Solver(
                data=aocd.get_data(day=day, year=year)
            ).part1()
            part1_runtime_obj = runtime
        CONSOLE.log(f"Part1: {solution}")
        submit(solution, part=ProblemPart.PART1, day=day, year=year)

    if not skip_part2:
        if not skip_tests:
            RichTestRunner(tb_locals=log_locals).make_suite_and_run(
                tests_module.PartTwoUnitTests
            )
        with log_runtime("Part 2", console=CONSOLE) as runtime:
            solution = solution_module.Solver(
                data=aocd.get_data(day=day, year=year)
            ).part2()
            part2_runtime_obj = runtime
        CONSOLE.log(f"Part2: {solution}")
        submit(solution, part=ProblemPart.PART2, day=day, year=year)

    print_runtime_table(part1_runtime_obj, part2_runtime_obj, CONSOLE)


if __name__ == "__main__":
    cli()
