#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from itertools import cycle
from math import lcm


class Solver(BaseSolver):
    PART1_EXAMPLE_SOLUTION: Solution | None = 2
    PART2_EXAMPLE_SOLUTION: Solution | None = 6

    def part1(self) -> Solution:
        return self.compute_answer(False)

    def part2(self) -> Solution:
        return self.compute_answer(True)

    def compute_answer(
        self,
        match_last_z: bool,
    ) -> int:
        direction_sequence, instructions = self.data.split("\n\n")

        node_to_directions = {}
        for line in instructions.splitlines():
            for c in "=(,)":
                line = line.replace(c, " ")
            node, left, right = line.split()
            node_to_directions[node] = (left, right)

        if match_last_z:
            nodes = [node for node in node_to_directions.keys() if node[-1] == "A"]
        else:
            nodes = ["AAA"]

        steps_to_z = []
        for node in nodes:
            steps = 0
            for dir in cycle(direction_sequence):
                if dir == "L":
                    node = node_to_directions[node][0]
                else:
                    node = node_to_directions[node][1]
                steps += 1
                if (match_last_z and node[-1] == "Z") or node == "ZZZ":
                    break
            steps_to_z.append(steps)
        return lcm(*steps_to_z)
