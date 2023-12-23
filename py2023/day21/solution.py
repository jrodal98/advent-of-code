#!/usr/bin/env python3
# www.jrodal.com

import numpy as np

from collections import deque

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Point


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        if self._is_unit_test:
            return self._compute_num_visited_after_steps(
                target_steps=6, allow_overflow=False
            )[0]
        else:
            return self._compute_num_visited_after_steps(
                target_steps=64, allow_overflow=False
            )[0]

    def _part2(self) -> Solution:
        if self._is_unit_test:
            return self._compute_num_visited_after_steps(
                target_steps=100, allow_overflow=True
            )[0]
        v1, v2, v3 = self._compute_num_visited_after_steps(
            target_steps=[65, 65 + 131, 65 + 131 * 2], allow_overflow=True
        )

        # shamelessly stolen from https://gist.github.com/dllu/0ca7bfbd10a199f69bcec92f067ec94c
        vandermonde = np.matrix([[0, 0, 1], [1, 1, 1], [4, 2, 1]])
        b = np.array([v1, v2, v3])
        x = np.linalg.solve(vandermonde, b).astype(np.int64)
        n = 202300
        return x[0] * n * n + x[1] * n + x[2]

    def _compute_num_visited_after_steps(
        self, target_steps: int | list[int], allow_overflow: bool
    ) -> list[int]:
        if isinstance(target_steps, int):
            target_steps = [target_steps]

        maximum_steps_allowed = max(target_steps)

        visited = set()
        places_to_go: deque[tuple[Point, int]] = deque([(self.grid.find("S"), 0)])
        while places_to_go:
            current_place, steps_taken = places_to_go.popleft()
            if (current_place, steps_taken) in visited:
                continue
            visited.add((current_place, steps_taken))
            if steps_taken == maximum_steps_allowed:
                continue

            for _, neighbor_p, _ in self.grid.neighbors(
                current_place, disqualify="#", allow_overflow=allow_overflow
            ):
                places_to_go.append(
                    (
                        neighbor_p,
                        steps_taken + 1,
                    )
                )
        return [sum(steps == target for _, steps in visited) for target in target_steps]
