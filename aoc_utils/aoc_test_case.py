#!/usr/bin/env python3
# www.jrodal.com

import os
import unittest
import yaml

from abc import ABC
from dataclasses import dataclass
from typing import Type

from aoc_utils.base_solver import BaseSolver, ProblemPart, Solution


PART1_TEST_SECTION = "part1"
PART2_TEST_SECTION = "part2"


@dataclass
class TestCaseFromManifest:
    input: str
    output: Solution
    name: str | None = None

    @classmethod
    def parse_manifest(
        cls, manifest_path: str, problem_part: ProblemPart
    ) -> list["TestCaseFromManifest"]:
        match problem_part:
            case ProblemPart.PART1:
                test_section = PART1_TEST_SECTION
            case ProblemPart.PART2:
                test_section = PART2_TEST_SECTION
            case _:
                raise Exception("Problem part must be specified")

        with open(manifest_path) as f:
            manifest = yaml.safe_load(f)
        return [cls(**test_case) for test_case in manifest.get(test_section, [])]


class AOCTestCase(unittest.TestCase, ABC):
    _PROBLEM_PART: ProblemPart
    _SOLVER: Type[BaseSolver]
    _DATA_DIR: str
    _MANIFEST_PATH: str

    def setUp(self) -> None:
        self.testcases = TestCaseFromManifest.parse_manifest(
            self._MANIFEST_PATH, self._PROBLEM_PART
        )

    def test_no_empty_inputs(self) -> None:
        for test in self.testcases:
            name = test.name or test.input
            with self.subTest(name=name):
                test_input = self._read_input(test)
                self.assertNotEqual(len(test_input), 0, msg=f"Test {name} is empty")

    def test_no_none_outputs(self) -> None:
        for test in self.testcases:
            name = test.name or test.input
            with self.subTest(name=name):
                self.assertIsNotNone(
                    test.output, msg=f"Test {name} had no expected output"
                )

    def _read_input(self, test: TestCaseFromManifest) -> str:
        if os.path.exists(os.path.join(self._DATA_DIR, test.input)):
            with open(os.path.join(self._DATA_DIR, test.input)) as f:
                return f.read()
        else:
            return test.input

    def test_execute_manifest(self) -> None:
        for test in self.testcases:
            name = test.name or test.input
            with self.subTest(name=name):
                if test.output is None:
                    continue

                test_input = self._read_input(test)
                if len(test_input) == 0:
                    continue

                solver = self._SOLVER(test_input, is_unit_test=True)
                match self._PROBLEM_PART:
                    case ProblemPart.PART1:
                        solution = solver.part1()
                    case ProblemPart.PART2:
                        solution = solver.part2()
                    case _:
                        raise Exception("Problem part must be specified")

                expected_output = test.output

                self.assertEqual(
                    expected_output,
                    solution,
                    f"Test {name}: {expected_output=}, {solution=}",
                )
