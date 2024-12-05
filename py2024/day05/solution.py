#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from collections import defaultdict

import functools


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return self._compute_scores()[0]

    def _part2(self) -> Solution:
        return self._compute_scores()[1]

    @functools.cache
    def _compute_scores(self) -> tuple[int, int]:
        rules, updates = self.data.split("\n\n")
        rule_dict = defaultdict(set)

        for rule in rules.splitlines():
            before, after = rule.split("|")
            rule_dict[before].add(after)

        in_order_score = 0
        out_of_order_score = 0

        for update in updates.splitlines():
            unsorted_nums = [n for n in update.split(",")]
            sorted_nums = sorted(
                unsorted_nums,
                key=functools.cmp_to_key(lambda a, b: -int(b in rule_dict[a])),
            )

            score = int(sorted_nums[len(sorted_nums) // 2])

            if unsorted_nums == sorted_nums:
                in_order_score += score
            else:
                out_of_order_score += score
        return in_order_score, out_of_order_score
