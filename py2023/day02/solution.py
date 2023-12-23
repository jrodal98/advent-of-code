#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    PART1_EXAMPLE_SOLUTION: Solution | None = 8
    PART2_EXAMPLE_SOLUTION: Solution | None = 2286

    def _part1(self) -> Solution:
        res = 0
        for game_id, line in enumerate(self.data.splitlines(), 1):
            bad = False
            _, sets = line.split(": ")
            sets = sets.split("; ")
            for st in sets:
                if bad:
                    break
                color_strings = st.split(", ")
                for cs in color_strings:
                    n, col = cs.split()
                    n = int(n)
                    if (
                        (col == "red" and n > 12)
                        or (col == "green" and n > 13)
                        or (col == "blue" and n > 14)
                    ):
                        bad = True
                        break
            if not bad:
                res += game_id

        return res

    def _part2(self) -> Solution:
        res = 0
        for line in self.data.splitlines():
            max_color_counts = {"red": 0, "blue": 0, "green": 0}
            _, sets = line.split(": ")
            sets = sets.split("; ")
            for st in sets:
                color_strings = st.split(", ")
                for cs in color_strings:
                    n, col = cs.split()
                    n = int(n)
                    max_color_counts[col] = max(n, max_color_counts[col])
            res += (
                max_color_counts["red"]
                * max_color_counts["blue"]
                * max_color_counts["green"]
            )

        return res
