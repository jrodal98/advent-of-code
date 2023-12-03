#!/usr/bin/env python3
# www.jrodal.com

import os
from .solution import Solver


class TestRunner:
    DATA_DIR = f"{os.path.dirname(__file__)}/data"

    def __init__(self) -> None:
        with open(f"{self.DATA_DIR}/part1_sample.txt") as f:
            self.part1_data = f.read()
        with open(f"{self.DATA_DIR}/part2_sample.txt") as f:
            self.part2_data = f.read() or self.part1_data

        if not self.part1_data:
            raise ValueError("part1_sample.txt is empty")

    def part1(self) -> None:
        solver = Solver(self.part1_data)
        example_solution = solver.PART1_EXAMPLE_SOLUTION
        assert example_solution is not None
        assert solver.part1() == example_solution

    def part2(self) -> None:
        solver = Solver(self.part2_data)
        example_solution = solver.PART2_EXAMPLE_SOLUTION
        assert example_solution is not None
        assert solver.part2() == example_solution
