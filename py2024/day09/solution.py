#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution

from dataclasses import dataclass


@dataclass
class Block:
    id: int | None
    count: int


class Solver(BaseSolver):
    def push_nones_to_back(self, lst: list[Block]) -> list[Block]:
        left = 0
        right = len(lst) - 1

        while left < right:
            while left < right and lst[left].id is not None:
                left += 1
            while left < right and lst[right].id is None:
                right -= 1
            if left < right:
                lst[left], lst[right] = lst[right], lst[left]
                left += 1
                right -= 1

        return lst

    def _part1(self) -> Solution:
        numbers = [int(n) for n in self.data]
        files_counts, free_spaces = numbers[::2], numbers[1::2]
        if len(files_counts) != len(free_spaces):
            free_spaces = free_spaces + [0]
        res = []
        for i, (files_count, free_space) in enumerate(zip(files_counts, free_spaces)):
            for _ in range(files_count):
                res.append(Block(id=i, count=1))
            for _ in range(free_space):
                res.append(Block(id=None, count=1))

        res = [x.id or 0 for x in self.push_nones_to_back(res)]

        ans = 0
        for i, v in enumerate(res):
            ans += i * v

        return ans

    def _part2(self) -> Solution:
        numbers = [int(n) for n in self.data]
        files_counts, free_spaces = numbers[::2], numbers[1::2]
        if len(files_counts) != len(free_spaces):
            free_spaces = free_spaces + [0]
        res = []
        # [2, 3, 1, 3, 2, 4, 4, 3, 4, 2]
        # [3, 3, 3, 1, 1, 1, 1, 1, 0, 0]

        left = 0
        right = len(files_counts) - 1
        while free_spaces and left < right:
            for _ in range(files_counts[left]):
                res.append(left)
            left += 1
            for i, free_space in enumerate(free_spaces.copy()):
                if files_counts[right] <= free_space:
                    for _ in range(files_counts[right]):
                        res.append(right)
                        free_spaces[i] -= 1
                    break
            right -= 1

        ans = 0
        for i, v in enumerate(res):
            ans += i * v

        return ans
