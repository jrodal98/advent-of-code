#!/usr/bin/env python3
# www.jrodal.com

import importlib
import os
import shutil
from types import ModuleType
import click
import aocd

from enum import Enum

from rich.console import Console
from rich.progress import SpinnerColumn
from rich.progress import Progress, MofNCompleteColumn, TimeElapsedColumn
from rich.traceback import install

from aoc_utils.solution_submitter import ProblemPart, submit
from aoc_utils.walk_directory import walk_directory



# override this if you are solving for other years
YEAR = aocd.get.most_recent_year()
DAY = aocd.get.current_day()
console = Console()


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
    console.log("AOC Solver!", log_locals=True)
    p = gen_solution_dir(day, year)
    shutil.copytree("templates", p)
    walk_directory(p, console)


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
    console.log("AOC Solver!", log_locals=True)

    install(suppress=[click], show_locals=log_locals)

    tasks = []
    if not skip_part1:
        if not skip_tests:
            tasks.append(Task.RUN_PART1_TESTS)
        tasks.append(Task.SOLVE_PART1)

    if not skip_part2:
        if not skip_tests:
            tasks.append(Task.RUN_PART2_TESTS)
        tasks.append(Task.SOLVE_PART2)

    module_path = gen_solution_dir(day, year).replace("/", ".")

    tests_module = importlib.import_module(f"{module_path}.tests")
    solution_module = importlib.import_module(f"{module_path}.solution")

    progress = Progress(
        SpinnerColumn(),
        TimeElapsedColumn(),
        MofNCompleteColumn(),
        console=console,
    )
    with progress:
        for task in progress.track(tasks):
            console.log(f"Running {task.value}")
            run_task(task, day, year, tests_module, solution_module, log_locals)
            console.log(f"{task.value} complete")


def run_task(
    task: Task,
    day: int,
    year: int,
    tests_module: ModuleType,
    solution_module: ModuleType,
    log_locals: bool
) -> None:
    match task:
        case Task.RUN_PART1_TESTS:
            tests_module.TestRunner.part1(log_locals)
        case Task.SOLVE_PART1:
            solution = solution_module.Solver(
                data=aocd.get_data(day=day, year=year)
            ).part1()
            submit(solution, part=ProblemPart.PART1, day=day, year=year)
        case Task.RUN_PART2_TESTS:
            tests_module.TestRunner.part2(log_locals)
        case Task.SOLVE_PART2:
            solution = solution_module.Solver(
                data=aocd.get_data(day=day, year=year)
            ).part2()
            submit(solution, part=ProblemPart.PART2, day=day, year=year)


if __name__ == "__main__":
    cli()
