#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    def push_nones_to_back(self, lst: list[int]):
        left = 0
        right = len(lst) - 1

        while left < right:
            while left < right and lst[left] is not None:
                left += 1
            while left < right and lst[right] is None:
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
                res.append(i)
            for _ in range(free_space):
                res.append(None)

        res = [x or 0 for x in self.push_nones_to_back(res)]

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
        all_nums = []
        for i, (files_count, free_space) in enumerate(zip(files_counts, free_spaces)):
            all_nums.append((i, files_count, len(res)))
            for _ in range(files_count):
                res.append(i)
            for _ in range(free_space):
                res.append(None)
        all_nums = all_nums[::-1]
        for id, window_size, starting_index in all_nums:
            for i in range(len(res) - window_size + 1):
                if i >= starting_index:
                    break
                window = res[i : i + window_size]
                if all(v is None for v in window):
                    res[starting_index : starting_index + window_size] = [
                        None
                    ] * window_size
                    res[i : i + window_size] = [id] * window_size
                    break

        print(res)
        ans = 0
        for i, v in enumerate(res):
            ans += i * (v or 0)

        return ans
