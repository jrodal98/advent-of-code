#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from itertools import cycle


class Solver(BaseSolver):
    PART1_EXAMPLE_SOLUTION: Solution | None = 2
    PART2_EXAMPLE_SOLUTION: Solution | None = 6

    def part1(self) -> Solution:
        direction_sequence, instructions = self.data.split("\n\n")

        node_to_directions = {}
        for line in instructions.splitlines():
            for c in "=(,)":
                line = line.replace(c, " ")
            node, left, right = line.split()
            node_to_directions[node] = (left, right)

        node = "AAA"
        steps = 0
        for dir in cycle(direction_sequence):
            if dir == "L":
                node = node_to_directions[node][0]
            else:
                node = node_to_directions[node][1]
            steps += 1
            if node == "ZZZ":
                break
        return steps

    def part2(self) -> Solution:
        direction_sequence, instructions = self.data.split("\n\n")

        node_to_directions = {}
        for line in instructions.splitlines():
            for c in "=(,)":
                line = line.replace(c, " ")
            node, left, right = line.split()
            node_to_directions[node] = (left, right)

        nodes = [node for node in node_to_directions.keys() if node[-1] == "A"]
        steps = 0
        for dir in cycle(direction_sequence):
            if dir == "L":
                nodes = [node_to_directions[node][0] for node in nodes]
            else:
                nodes = [node_to_directions[node][1] for node in nodes]
            steps += 1
            if all(node[-1] == "Z" for node in nodes):
                break
        return steps
