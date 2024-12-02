#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    def _is_level_safe(self, level: str) -> bool:
        nums = [int(n) for n in level.split()]
        has_increased = False
        has_decreased = False
        for prev, cur in zip(nums, nums[1:]):
            diff = abs(cur - prev)
            if diff < 1 or diff > 3:
                return False

            has_increased = has_increased or cur > prev
            has_decreased = has_decreased or cur < prev

            if has_increased and has_decreased:
                return False

        return True

    def _part1(self) -> Solution:
        return sum(self._is_level_safe(level) for level in self.lines())

    def _part2(self) -> Solution:
        safe = 0
        for line in self.lines():
            nums = [int(n) for n in line.split()]
            for index_to_skip in range(len(nums) + 1):
                nums_to_process = nums.copy()
                if index_to_skip < len(nums):
                    nums_to_process.pop(index_to_skip)
                all_increasing = True
                all_decreasing = True
                safe_dropoff = True
                last_num = None
                for num in nums_to_process:
                    if last_num is None:
                        last_num = num
                        continue
                    all_increasing = all_increasing and (num > last_num)
                    all_decreasing = all_decreasing and (num < last_num)
                    diff = abs(num - last_num)
                    safe_dropoff = safe_dropoff and diff in (1, 2, 3)
                    last_num = num
                if safe_dropoff and (all_increasing or all_decreasing):
                    safe += 1
                    break

        return safe
