#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    PART1_EXAMPLE_SOLUTION: Solution | None = 4361
    PART2_EXAMPLE_SOLUTION: Solution | None = 467835

    def part1(self) -> Solution:
        grid = []
        for line in self.data.splitlines():
            row = []
            for c in line:
                row.append(c)
            grid.append(row)
        good_pairs = set()
        checked_pairs = set()
        for row_i, row_v in enumerate(grid):
            for col_i, cell in enumerate(row_v):
                if not cell.isdigit() and cell != ".":
                    good_pairs.add((row_i - 1, col_i))
                    good_pairs.add((row_i + 1, col_i))
                    good_pairs.add((row_i, col_i - 1))
                    good_pairs.add((row_i, col_i + 1))
                    good_pairs.add((row_i + 1, col_i + 1))
                    good_pairs.add((row_i - 1, col_i + 1))
                    good_pairs.add((row_i + 1, col_i - 1))
                    good_pairs.add((row_i - 1, col_i - 1))
        nums = []
        for row_i, col_j in good_pairs:
            if (row_i, col_j) in checked_pairs:
                continue
            try:
                c = grid[row_i][col_j]
                checked_pairs.add((row_i, col_j))
                if not c.isdigit():
                    continue
            except Exception:
                continue
            before = ""
            after = ""
            co = col_j - 1
            while co > -1:
                a = grid[row_i][co]
                checked_pairs.add((row_i, co))
                co -= 1
                if a.isdigit():
                    before = a + before
                else:
                    break
            co = col_j + 1
            while co < len(grid[0]):
                a = grid[row_i][co]
                checked_pairs.add((row_i, co))
                co += 1
                if a.isdigit():
                    after = after + a
                else:
                    break

            nums.append(int(before + c + after))

        return sum(nums)

    def part2(self) -> Solution:
        grid = []
        for line in self.data.splitlines():
            row = []
            for c in line:
                row.append(c)
            grid.append(row)
        good_pairs = {}
        checked_pairs = set()
        for row_i, row_v in enumerate(grid):
            for col_i, cell in enumerate(row_v):
                if cell == "*":
                    good_pairs[(row_i, col_i)] = [
                        (row_i - 1, col_i),
                        (row_i + 1, col_i),
                        (row_i, col_i - 1),
                        (row_i, col_i + 1),
                        (row_i + 1, col_i + 1),
                        (row_i - 1, col_i + 1),
                        (row_i + 1, col_i - 1),
                        (row_i - 1, col_i - 1),
                    ]
        res = 0
        for v in good_pairs.values():
            nums = []
            for row_i, col_j in v:
                if (row_i, col_j) in checked_pairs:
                    continue
                try:
                    c = grid[row_i][col_j]
                    checked_pairs.add((row_i, col_j))
                    if not c.isdigit():
                        continue
                except Exception:
                    continue
                before = ""
                after = ""
                co = col_j - 1
                while co > -1:
                    a = grid[row_i][co]
                    checked_pairs.add((row_i, co))
                    co -= 1
                    if a.isdigit():
                        before = a + before
                    else:
                        break
                co = col_j + 1
                while co < len(grid[0]):
                    a = grid[row_i][co]
                    checked_pairs.add((row_i, co))
                    co += 1
                    if a.isdigit():
                        after = after + a
                    else:
                        break

                nums.append(int(before + c + after))
            if len(nums) == 2:
                res += nums[0] * nums[1]

        return res
