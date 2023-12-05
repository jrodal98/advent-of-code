#!/usr/bin/env python3
# www.jrodal.com

import re
from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    PART1_EXAMPLE_SOLUTION: Solution | None = 35
    PART2_EXAMPLE_SOLUTION: Solution | None = None

    def part1(self) -> Solution:
        lines = self.data.split("\n\n")
        seeds_line = lines[0]
        map_lines = lines[1:]
        seeds = [int(i) for i in re.findall(r"\d+", seeds_line)]
        final_seeds = []
        for line in map_lines:
            _, *numbers = line.splitlines()
            working_seeds = seeds.copy()
            new_seeds = []
            for range_info in numbers:
                ds, ss, rl = [int(i) for i in range_info.split()]
                new_working_seeds = []
                for seed in working_seeds:
                    if ss <= seed < ss + rl:
                        new_seeds.append(seed + ds - ss)
                    else:
                        new_working_seeds.append(seed)
                working_seeds = new_working_seeds
            final_seeds.extend(new_seeds)
            seeds = new_seeds + working_seeds
        return min(seeds)

    def part2(self) -> Solution:
        pass

    #     lines = self.data.split("\n\n")
    #     seeds_line = lines[0]
    #     map_lines = lines[1:]
    #     seeds = [int(i) for i in re.findall(r"\d+", seeds_line)]
    #     seed_ranges = list(zip(seeds[::2], seeds[1::2]))
    #     for line in map_lines:
    #         _, *numbers = line.splitlines()
    #         working_seeds = seeds.copy()
    #         new_ranges = []
    #         for range_info in numbers:
    #             ds, ss, rl = [int(i) for i in range_info.split()]
    #             new_working_seeds = []
    #             for seed in working_seeds:
    #                 if ss <= seed < ss + rl:
    #                     new_seeds.append(seed + ds - ss)
    #                 else:
    #                     new_working_seeds.append(seed)
    #             working_seeds = new_working_seeds
    #         seeds = new_seeds + working_seeds
    #     return min(seeds)
