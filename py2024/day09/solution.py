#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        numbers = [int(n) for n in self.data]
        files_counts, free_spaces = numbers[::2], numbers[1::2]
        if len(files_counts) != len(free_spaces):
            free_spaces.append(0)
        filesystem = []
        for i, (files_count, free_space) in enumerate(zip(files_counts, free_spaces)):
            for _ in range(files_count):
                filesystem.append(i)
            for _ in range(free_space):
                filesystem.append(None)

        left = 0
        right = len(filesystem) - 1

        while left < right:
            while left < right and filesystem[left] is not None:
                left += 1
            while left < right and filesystem[right] is None:
                right -= 1
            if left < right:
                filesystem[left], filesystem[right] = (
                    filesystem[right],
                    filesystem[left],
                )
                left += 1
                right -= 1

        return sum(i * (v or 0) for i, v in enumerate(filesystem))

    def _part2(self) -> Solution:
        numbers = [int(n) for n in self.data]
        files_counts, free_spaces = numbers[::2], numbers[1::2]
        if len(files_counts) != len(free_spaces):
            free_spaces.append(0)
        filesystem = []
        all_nums = []
        for i, (files_count, free_space) in enumerate(zip(files_counts, free_spaces)):
            all_nums.append((i, files_count, len(filesystem)))
            for _ in range(files_count):
                filesystem.append(i)
            for _ in range(free_space):
                filesystem.append(None)
        all_nums = all_nums[::-1]
        for id, window_size, file_start_index in all_nums:
            for window_start_index in range(len(filesystem) - window_size + 1):
                if window_start_index >= file_start_index:
                    break
                window = filesystem[
                    window_start_index : window_start_index + window_size
                ]
                if all(v is None for v in window):
                    filesystem[file_start_index : file_start_index + window_size] = [
                        None
                    ] * window_size
                    filesystem[
                        window_start_index : window_start_index + window_size
                    ] = [id] * window_size
                    break

        return sum(i * (v or 0) for i, v in enumerate(filesystem))
