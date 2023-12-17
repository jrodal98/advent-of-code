#!/usr/bin/env python3
# www.jrodal.com

import heapq
from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Direction, Point


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return self._compute(0, 3)

    def _part2(self) -> Solution:
        return self._compute(4, 10)

    def _compute(self, min_steps_forward: int, max_steps_forward: int) -> Solution:
        grid = self.grid.transform(lambda x: int(x))
        state = (0, Point(0, 0), Direction.RIGHT, 0)
        seen = set()
        queue = [state]
        best_so_far = sum(grid.data)
        while queue:
            (
                current_cost,
                current_pos,
                current_dir,
                current_steps_straight,
            ) = heapq.heappop(queue)
            state_key = (current_pos, current_dir, current_steps_straight)
            if state_key in seen:
                continue

            seen.add(state_key)
            if current_pos == Point(grid.w - 1, grid.h - 1):
                best_so_far = min(best_so_far, current_cost)
                continue

            if current_steps_straight < min_steps_forward:
                dirs = [current_dir]
            else:
                dirs = [current_dir.clockwise, current_dir.counter_clockwise]
                if current_steps_straight < max_steps_forward:
                    dirs.append(current_dir)

            for d in dirs:
                next_pos = current_pos.neighbor(d)
                next_cost = grid.get(next_pos)
                if not next_cost:
                    continue
                cost_so_far = current_cost + next_cost
                heapq.heappush(
                    queue,  # pyright: ignore
                    (
                        cost_so_far,
                        next_pos,
                        d,
                        1 if current_dir is not d else current_steps_straight + 1,
                    ),
                )
        return best_so_far
