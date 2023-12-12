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
        consume_pounds = record[1:].lstrip("#")
        ans += num_valid(
            consume_pounds,
            nums,
            n_damaged + len(record) - len(consume_pounds),
        )
    if c in [".", "?"]:
        if n_damaged not in [0, target]:
            return ans

        consume_dots = record[1:].lstrip(".")
        consume_dots_and_pounds = consume_dots.lstrip("#")
        ans += num_valid(
            consume_dots_and_pounds,
            nums[int(n_damaged > 0) :],
            len(consume_dots) - len(consume_dots_and_pounds),
        )
    return ans


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        res = 0
        for line in self.data.splitlines():
            record, nums = line.split()
            nums = tuple(int(i) for i in nums.split(","))
            consume_dots = record.strip(".")
            consume_dots_and_pounds = consume_dots.lstrip("#")
            res += num_valid(
                consume_dots_and_pounds,
                nums,
                len(consume_dots) - len(consume_dots_and_pounds),
            )
        return res

    def _part2(self) -> Solution:
        res = 0
        for line in self.data.splitlines():
            record, nums = line.split()
            record = "?".join([record] * 5)
            nums = ",".join([nums] * 5)
            nums = tuple(int(i) for i in nums.split(","))
            consume_dots = record.strip(".")
            consume_dots_and_pounds = consume_dots.lstrip("#")
            res += num_valid(
                consume_dots_and_pounds,
                nums,
                len(consume_dots) - len(consume_dots_and_pounds),
            )
        return res
