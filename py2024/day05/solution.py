#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from collections import defaultdict

import functools


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        rules, updates = self.data.split("\n\n")
        rule_dict = defaultdict(set)

        for rule in rules.splitlines():
            before, after = rule.split("|")
            rule_dict[int(before)].add(int(after))

        ans = 0
        for update in updates.splitlines():
            nums = [int(n) for n in update.split(",")]
            if self._is_in_order(nums, rule_dict):
                ans += nums[len(nums) // 2]
        return ans

    def _is_in_order(
        self, nums: list[int], rule_dict: defaultdict[int, set[int]]
    ) -> bool:
        for i, num in enumerate(nums):
            nums_after = nums[i + 1 :]
            if any(num in rule_dict[n] for n in nums_after):
                return False
        return True

    def _sort_nums(
        self, nums: list[int], rule_dict: defaultdict[int, set[int]]
    ) -> list[int]:
        def compare(a, b):
            if b in rule_dict[a]:
                return -1
            else:
                return 0

        x = sorted(nums, key=functools.cmp_to_key(compare))
        print(nums, x)
        return x

    def _part2(self) -> Solution:
        rules, updates = self.data.split("\n\n")
        rule_dict = defaultdict(set)

        for rule in rules.splitlines():
            before, after = rule.split("|")
            rule_dict[int(before)].add(int(after))

        ans = 0
        for update in updates.splitlines():
            nums = [int(n) for n in update.split(",")]

            if not self._is_in_order(nums, rule_dict):
                nums = self._sort_nums(nums, rule_dict)
                ans += nums[len(nums) // 2]
        return ans
