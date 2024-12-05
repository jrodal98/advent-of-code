#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from collections import defaultdict


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        rules, updates = self.data.split("\n\n")
        violations = defaultdict(set)

        for rule in rules.splitlines():
            before, after = rule.split("|")
            violations[int(after)].add(int(before))

        ans = 0
        for update in updates.splitlines():
            nums = [int(n) for n in update.split(",")]
            if self._is_in_order(nums, violations):
                ans += nums[len(nums) // 2]
        return ans

    def _is_in_order(
        self, nums: list[int], violations: defaultdict[int, set[int]]
    ) -> bool:
        for i, num in enumerate(nums):
            nums_after = nums[i + 1 :]
            if not all(num in violations[n] for n in nums_after):
                return False
        return True

    def _sort_nums(
        self, nums: list[int], violations: defaultdict[int, set[int]]
    ) -> list[int]:
        new_nums = []
        for i, num in enumerate(nums):
            nums_after = nums[i + 1 :]
            for n in nums_after:
                if num in violations[n]:
                    new_nums.append(n)
                    break
        return new_nums

    def _part2(self) -> Solution:
        rules, updates = self.data.split("\n\n")
        violations = defaultdict(set)

        for rule in rules.splitlines():
            before, after = rule.split("|")
            violations[int(after)].add(int(before))

        ans = 0
        for update in updates.splitlines():
            correctly_ordered = True
            nums = [int(n) for n in update.split(",")]

            if not correctly_ordered:
                nums = self._sort_nums(nums, violations)
                ans += nums[len(nums) // 2]
        return ans
