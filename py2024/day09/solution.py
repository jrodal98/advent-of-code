#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        numbers = [int(n) for n in self.data]
        files_counts, free_spaces = numbers[::2], numbers[1::2]
        if len(files_counts) != len(free_spaces):
            free_spaces.append(0)
        res = []
        for i, (files_count, free_space) in enumerate(zip(files_counts, free_spaces)):
            for _ in range(files_count):
                res.append(i)
            for _ in range(free_space):
                res.append(None)

        left = 0
        right = len(res) - 1

        while left < right:
            while left < right and res[left] is not None:
                left += 1
            while left < right and res[right] is None:
                right -= 1
            if left < right:
                res[left], res[right] = res[right], res[left]
                left += 1
                right -= 1

        return sum(i * (v or 0) for i, v in enumerate(res))

    def _part2(self) -> Solution:
        numbers = [int(n) for n in self.data]
        files_counts, free_spaces = numbers[::2], numbers[1::2]
        if len(files_counts) != len(free_spaces):
            free_spaces.append(0)
        res = []
        all_nums = []
        for i, (files_count, free_space) in enumerate(zip(files_counts, free_spaces)):
            all_nums.append((i, files_count, len(res)))
            for _ in range(files_count):
                res.append(i)
            for _ in range(free_space):
                res.append(None)
        all_nums = all_nums[::-1]
        for id, window_size, file_start_index in all_nums:
            for window_start_index in range(len(res) - window_size + 1):
                if window_start_index >= file_start_index:
                    break
                window = res[window_start_index : window_start_index + window_size]
                if all(v is None for v in window):
                    res[file_start_index : file_start_index + window_size] = [
                        None
                    ] * window_size
                    res[window_start_index : window_start_index + window_size] = [
                        id
                    ] * window_size
                    break

        return sum(i * (v or 0) for i, v in enumerate(res))
