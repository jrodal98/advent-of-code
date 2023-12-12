#!/usr/bin/env python3
# www.jrodal.com


from functools import cache
from aoc_utils.base_solver import BaseSolver, Solution


@cache
def num_valid(
    record: str,
    nums: tuple[int, ...],
    n_damaged: int,
) -> int:
    target = nums[0] if nums else 0
    if n_damaged > target:
        return 0
    if not record:
        return sum(nums) == n_damaged

    ans = 0
    c = record[0]
    if c in ["#", "?"]:
        ans += num_valid(record[1:], nums, n_damaged + 1)
    if c in [".", "?"]:
        if n_damaged == 0:
            ans += num_valid(record[1:].lstrip("."), nums, 0)
        elif n_damaged == target:
            ans += num_valid(record[1:].lstrip("."), nums[1:], 0)
    return ans


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        res = 0
        for line in self.data.splitlines():
            record, nums = line.split()
            nums = tuple(int(i) for i in nums.split(","))
            res += num_valid(record.lstrip(".").rstrip("."), nums, 0)
        return res

    def _part2(self) -> Solution:
        res = 0
        for line in self.data.splitlines():
            record, nums = line.split()
            record = "?".join([record] * 5)
            nums = ",".join([nums] * 5)
            nums = tuple(int(i) for i in nums.split(","))
            res += num_valid(record.lstrip(".").rstrip("."), nums, 0)
        return res
