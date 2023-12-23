#!/usr/bin/env python3
# www.jrodal.com

import re
from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    PART1_EXAMPLE_SOLUTION: Solution | None = 35
    PART2_EXAMPLE_SOLUTION: Solution | None = 46

    def _part1(self) -> Solution:
        lines = self.data.split("\n\n")
        seeds_line = lines[0]
        map_lines = lines[1:]
        seeds = [int(i) for i in re.findall(r"\d+", seeds_line)]
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
            seeds = new_seeds + working_seeds
        return min(seeds)

    def _part2(self) -> Solution:
        lines = self.data.split("\n\n")
        seeds_line = lines[0]
        map_lines = lines[1:]
        seeds = [int(i) for i in re.findall(r"\d+", seeds_line)]
        seed_ranges = list(zip(seeds[::2], seeds[1::2]))
        seed_ranges = [(s, s + e) for s, e in seed_ranges]
        for line in map_lines:
            _, *numbers = line.splitlines()
            working_ranges = seed_ranges.copy()
            new_ranges = []
            for range_info in numbers:
                ds, ss, rl = [int(i) for i in range_info.split()]
                new_working_ranges = []
                for s, f in working_ranges:
                    intersection_start = max(s, ss)
                    intersection_end = min(f, ss + rl)
                    if intersection_start <= intersection_end:
                        new_ranges.append(
                            (intersection_start + ds - ss, intersection_end + ds - ss)
                        )
                        if s < intersection_start:
                            new_working_ranges.append((s, intersection_start))
                        if intersection_end < f:
                            new_working_ranges.append((intersection_end, f))
                    else:
                        new_working_ranges.append((s, f))
                working_ranges = new_working_ranges
            seed_ranges = working_ranges + new_ranges
        return min(s for s, _ in seed_ranges)
