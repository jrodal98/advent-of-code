#!/usr/bin/env python3
# www.jrodal.com

from itertools import product
from aoc_utils.base_solver import BaseSolver, Solution


# @cache
def is_valid(record: str, nums: tuple[int]) -> bool:
    groups = [x for x in record.split(".") if x]
    if len(groups) != len(nums):
        return False
    for i, v in enumerate(groups):
        if len(v) != nums[i]:
            return False
    return True


def generate_permutations(input_string):
    # Replace '?' with possible characters
    possible_characters = set(["#", "."])
    replaced_string = [c if c != "?" else possible_characters for c in input_string]

    # Generate all possible permutations
    permutations = ["".join(p) for p in product(*replaced_string)]

    return permutations


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        res = 0
        for line in self.data.splitlines():
            record, nums = line.split()
            nums = tuple(int(i) for i in nums.split(","))
            for p in generate_permutations(record):
                is_v = is_valid(p, nums)
                res += int(is_v)
        return res

    def _part2(self) -> Solution:
        raise NotImplementedError
