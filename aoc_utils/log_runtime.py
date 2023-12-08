from dataclasses import dataclass
import time

from contextlib import contextmanager
from rich.console import Console
from typing import Generator

from rich.table import Table

from consts import CONSOLE


@dataclass
class Runtime:
    elapsed_time_unit: float | None
    unit: str | None
    elapsed_time_seconds: float | None


@contextmanager
def log_runtime(
    msg: str, *, console: Console = CONSOLE
) -> Generator[Runtime, None, None]:
    start_time = time.time()
    runtime = Runtime(None, None, None)
    yield runtime
    end_time = time.time()
    elapsed_time_seconds = end_time - start_time
    elapsed_time = elapsed_time_seconds
    if elapsed_time < 1e-3:
        unit = "μs"
        elapsed_time *= 1e6
    elif elapsed_time < 1:
        unit = "ms"
        elapsed_time *= 1e3
    elif elapsed_time < 60:
        unit = "s"
    elif elapsed_time < 3600:
        unit = "m"
        elapsed_time /= 60
    else:
        unit = "h"
        elapsed_time /= 3600

    console.log(f"{msg} executed in {elapsed_time:.2f} {unit}")
    runtime.elapsed_time_unit = elapsed_time
    runtime.unit = unit
    runtime.elapsed_time_seconds = elapsed_time_seconds


def print_runtime_table(
    part1_runtime_obj: Runtime | None,
    part2_runtime_obj: Runtime | None,
    console: Console | None,
) -> None:
    if not part1_runtime_obj and not part2_runtime_obj:
        return

    console = console or CONSOLE

    table = Table(show_header=True, header_style="bold magenta")

    table.add_column("Part", justify="center")
    table.add_column("Runtime", justify="center")
    table.add_column("Part2/Part1", justify="center")

    table.add_row(
        "1",
        f"{part1_runtime_obj.elapsed_time_unit:.2f} {part1_runtime_obj.unit}"
        if part1_runtime_obj
        else "X",
        "X",
    )

    part2_to_part1_ratio = "X"
    if (
        part1_runtime_obj
        and part2_runtime_obj
        and part2_runtime_obj.elapsed_time_seconds
        and part1_runtime_obj.elapsed_time_seconds
    ):
        ratio = (
            part2_runtime_obj.elapsed_time_seconds
            / part1_runtime_obj.elapsed_time_seconds
        )
        if ratio < 1:
            part2_to_part1_ratio = f"{ratio:.2f}x faster"
        else:
            part2_to_part1_ratio = f"{ratio:.2f}x slower"

    table.add_row(
        "2",
        f"{part2_runtime_obj.elapsed_time_unit:.2f} {part2_runtime_obj.unit}"
        if part2_runtime_obj
        else "X",
        part2_to_part1_ratio,
    )

    console.print(table)
