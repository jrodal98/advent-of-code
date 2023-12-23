#!/usr/bin/env python3
# www.jrodal.com

import re

from rich.progress import track
from aoc_utils.base_solver import BaseSolver, Solution

import numpy as np

EPSILON = 0.0001


class Solver(BaseSolver):
    PART1_EXAMPLE_SOLUTION: Solution | None = 288
    PART2_EXAMPLE_SOLUTION: Solution | None = 71503

    def find_scores(self, x: int) -> list[int]:
        scores = []
        for i in track(range(x + 1)):
            j = x - i
            scores.append(i * j)
        return scores

    # This is a math based solution that works in place of compute_num_wins
    def compute_num_wins_with_math(self, times: list[int], distances: list[int]) -> int:
        res = 1
        for time, distance in zip(times, distances):
            roots = np.roots([1, -time, distance + EPSILON])
            bigger, smaller = int(max(roots)), int(min(roots))
            res *= bigger - smaller
        return res

    # This is the solution I used during submission
    def compute_num_wins(self, times: list[int], distances: list[int]) -> int:
        result = 1
        for time, distance in zip(times, distances):
            scores = self.find_scores(time)
            res = 0
            for score in scores:
                if score > distance:
                    res += 1
            result *= res
        return result

    def _part1(self) -> Solution:
        times_line, distances_line = self.data.splitlines()
        times = [int(i) for i in re.findall(r"\d+", times_line)]
        distances = [int(i) for i in re.findall(r"\d+", distances_line)]

        return self.compute_num_wins_with_math(times, distances)
        # return self.compute_num_wins(times, distances)

    def _part2(self) -> Solution:
        times_line, distances_line = self.data.splitlines()
        times = [int("".join(re.findall(r"\d+", times_line)))]
        distances = [int("".join(re.findall(r"\d+", distances_line)))]

        return self.compute_num_wins_with_math(times, distances)
        # return self.compute_num_wins(times, distances)
