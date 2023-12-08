import time

from contextlib import contextmanager
from rich.console import Console
from typing import Generator

from consts import CONSOLE


@contextmanager
def log_runtime(msg: str, *, console: Console = CONSOLE) -> Generator[None, None, None]:
    start_time = time.time()
    yield
    end_time = time.time()
    elapsed_time = end_time - start_time
    if elapsed_time < 1e-3:
        unit = "microseconds"
        elapsed_time *= 1e6
    elif elapsed_time < 1:
        unit = "milliseconds"
        elapsed_time *= 1e3
    elif elapsed_time < 60:
        unit = "seconds"
    elif elapsed_time < 3600:
        unit = "minutes"
        elapsed_time /= 60
    else:
        unit = "hours"
        elapsed_time /= 3600

    console.log(f"{msg} executed in {elapsed_time:.4f} {unit}")
