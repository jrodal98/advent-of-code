#!/usr/bin/env python3
# www.jrodal.com

import os

from aoc_utils.aoc_test_case import AOCTestCase
from aoc_utils.base_solver import ProblemPart

from .solution import Solver


class PartOneUnitTests(AOCTestCase):
    _PROBLEM_PART = ProblemPart.PART1
    _SOLVER = Solver
    _DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
    _MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "test_manifest.yml")


class PartTwoUnitTests(AOCTestCase):
    _PROBLEM_PART = ProblemPart.PART2
    _SOLVER = Solver
    _DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
    _MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "test_manifest.yml")
