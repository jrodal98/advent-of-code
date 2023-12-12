#!/usr/bin/env python3
# www.jrodal.com

from itertools import product

from aoc_utils.base_solver import BaseSolver, Solution

num_cache_hits = 0
num_cache_misses = 0


def is_valid(
    record: str, nums: tuple[int, ...], cache: dict[tuple[str, tuple[int, ...]], bool]
) -> bool:
    global num_cache_hits, num_cache_misses
    if (record, nums) in cache:
        num_cache_hits += 1
        return cache[(record, nums)]

    num_cache_misses += 1

    groups = [x for x in record.split(".") if x]
    if len(groups) != len(nums):
        cache[(record, nums)] = False
        return False
    for i, v in enumerate(groups):
        if len(v) != nums[i]:
            cache[(record, nums)] = False
            return False
    cache[(record, nums)] = True
    return True


def generate_permutations(record, nums):
    # Replace '?' with possible characters
    possible_characters = set(["#", "."])
    replaced_string = [c if c != "?" else possible_characters for c in record]

    l_nums_minus_1 = len(nums) - 1
    s_nums = sum(nums)

    # Generate all possible permutations
    permutations = (
        "".join(p)
        for p in product(*replaced_string)
        if not (p.count(".") < l_nums_minus_1 or s_nums > p.count("#"))
    )

    return permutations


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        global num_cache_hits, num_cache_misses
        res = 0
        cache = {}
        for line in self.data.splitlines():
            record, nums = line.split()
            nums = tuple(int(i) for i in nums.split(","))
            for p in generate_permutations(record, nums):
                is_v = is_valid(p, nums, cache)
                res += int(is_v)
        print(
            f"Cache hits: {num_cache_hits * 100 / (num_cache_hits + num_cache_misses):.2f}%",
            f"{num_cache_hits=}",
            f"{num_cache_misses=}",
        )
        return res

    def _part2(self) -> Solution:
        res = 0
        cache = {}
        for line in self.data.splitlines():
            record, nums = line.split()
            record = "?".join([record] * 5)
            nums = ",".join([nums] * 5)
            nums = tuple(int(i) for i in nums.split(","))
            for p in generate_permutations(record, nums):
                is_v = is_valid(p, nums, cache)
                res += int(is_v)
        return res
