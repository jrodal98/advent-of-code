#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    def _init_filesystem(self) -> tuple[list[int | None], list[tuple[int, int, int]]]:
        numbers = [int(n) for n in self.data]
        # file_blocks, free_spaces = numbers[::2], numbers[1::2]
        # if len(file_blocks) != len(free_spaces):
        #     free_spaces.append(0)
        # filesystem = []
        # all_nums = []
        # for id, (num_blocks, free_space) in enumerate(zip(file_blocks, free_spaces)):
        #     all_nums.append((id, num_blocks, len(filesystem)))
        #     for _ in range(num_blocks):
        #         filesystem.append(id)
        #     for _ in range(free_space):
        #         filesystem.append(None)

        filesystem = []
        all_nums = []
        if len(numbers) % 2 == 1:
            numbers.append(0)
        for id, i in enumerate(range(0, len(numbers), 2)):
            all_nums.append((id, numbers[i], len(filesystem)))
            filesystem.extend([id] * numbers[i])
            filesystem.extend([None] * numbers[i + 1])

        return filesystem, all_nums[::-1]

    def _part1(self) -> Solution:
        filesystem, _ = self._init_filesystem()

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
        filesystem, all_nums = self._init_filesystem()
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
