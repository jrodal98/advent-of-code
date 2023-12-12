#!/usr/bin/env python3
# www.jrodal.com


from aoc_utils.base_solver import BaseSolver, Solution


# @cache
def num_valid(
    record: str,
    nums: tuple[int, ...],
    n_damaged: int,
) -> int:
    if not record:
        if len(nums) > 1:
            return 0
        elif len(nums) == 1:
            return int(nums[0] == n_damaged)
        elif n_damaged == 0:
            return 1
        else:
            return 0

    # ?###???????? 3,2,1
    target = nums[0] if nums else 0
    for i, c in enumerate(record):
        if n_damaged > target:
            return 0
        if c == "#":
            if n_damaged == target:
                return 0
            n_damaged += 1
        elif c == "?":
            ans = 0
            if n_damaged == target:
                # only valid option is .
                x = num_valid(record[i + 1 :], nums[1:], 0)
                # print(f"num valid when {record[i :]} is .: {x}")
                ans += x
            else:
                # replace with a #
                x = num_valid(record[i + 1 :], nums, n_damaged + 1)
                # print(f"num valid when {record[i :]} is #: {x}")
                ans += x

            if not n_damaged and target != 0:
                # if there is no damage, we can "skip" this one
                x = num_valid(record[i + 1 :], nums, 0)
                ans += x

            return ans
        else:
            if not n_damaged:
                continue
            if n_damaged != target:
                return 0
            nums = nums[1:]
            target = nums[0] if nums else 0
            n_damaged = 0

    if n_damaged != target:
        return 0

    return 1


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        res = 0
        for line in self.data.splitlines():
            record, nums = line.split()
            nums = tuple(int(i) for i in nums.split(","))
            res += num_valid(record, nums, 0)
        return res

    def _part2(self) -> Solution:
        res = 0
        for line in self.data.splitlines():
            record, nums = line.split()
            record = "?".join([record] * 5)
            nums = ",".join([nums] * 5)
            nums = tuple(int(i) for i in nums.split(","))
            res += num_valid(record, nums, 0)
        return res
