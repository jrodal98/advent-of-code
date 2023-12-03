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
        example_solution = None
        assert example_solution is not None

        assert Solver(self.part1_data).part1() == example_solution

    def part2(self) -> None:
        example_solution = None
        assert example_solution is not None

        assert Solver(self.part2_data).part2() == example_solution
