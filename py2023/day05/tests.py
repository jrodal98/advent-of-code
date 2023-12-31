#!/usr/bin/env python3
# www.jrodal.com

import os
import unittest

from .solution import Solver


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PART1_SAMPLE_PATH = os.path.join(DATA_DIR, "part1_sample.txt")
PART2_SAMPLE_PATH = os.path.join(DATA_DIR, "part2_sample.txt")


class PartOneUnitTests(unittest.TestCase):
    def setUp(self) -> None:
        with open(PART1_SAMPLE_PATH) as f:
            self.data = f.read()

    def test_example_input_not_empty(self) -> None:
        self.assertTrue(len(self.data) > 0, f"{PART1_SAMPLE_PATH} is empty!")

    def test_example_input(self) -> None:
        solver = Solver(self.data)
        example_solution = solver.PART1_EXAMPLE_SOLUTION
        self.assertIsNotNone(example_solution, "Example solution not filled out!")
        part1_solution = solver.part1()
        self.assertEqual(
            part1_solution, example_solution, f"{part1_solution=}, {example_solution=}"
        )


class PartTwoUnitTests(unittest.TestCase):
    def setUp(self) -> None:
        with open(PART2_SAMPLE_PATH) as f:
            self.data = f.read()
        if not self.data:
            with open(PART1_SAMPLE_PATH) as f:
                self.data = f.read()

    def test_example_input_not_empty(self) -> None:
        self.assertTrue(
            len(self.data) > 0, f"{PART2_SAMPLE_PATH} and {PART1_SAMPLE_PATH} empty!"
        )

    def test_example_input(self) -> None:
        solver = Solver(self.data)
        example_solution = solver.PART2_EXAMPLE_SOLUTION
        self.assertIsNotNone(example_solution, "Example solution not filled out!")
        part2_solution = solver.part2()
        self.assertEqual(
            part2_solution, example_solution, f"{part2_solution=}, {example_solution=}"
        )
