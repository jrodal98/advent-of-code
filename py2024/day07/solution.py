#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    def _helper(self, concat: bool) -> int:
        ans = 0
        for line in self.lines():
            test_value, nums = line.split(": ")
            test_value = int(test_value)
            nums = [int(n) for n in nums.split()]
            possible_values = [nums[0]]
            for num in nums[1:]:
                new_possible_values = []
                for possible_value in possible_values:
                    new_possible_values.append(possible_value + num)
                    new_possible_values.append(possible_value * num)
                    if concat:
                        new_possible_values.append(int(str(possible_value) + str(num)))
                possible_values = new_possible_values
            if test_value in possible_values:
                ans += test_value

        return ans

    def _part1(self) -> Solution:
        return self._helper(False)

    def _part2(self) -> Solution:
        return self._helper(True)
