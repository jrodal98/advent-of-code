#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Direction, Point
from collections import deque


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        grid = self.grid.transform(lambda x: int(x))
        state = ((Point(0, 0), Direction.RIGHT, 0), 0)
        seen = {}
        queue = deque([state])
        best_so_far = float("inf")
        while queue:
            state_key, current_cost = queue.popleft()
            if state_key in seen and current_cost >= seen[state_key]:
                continue
            (
                current_pos,
                current_dir,
                current_steps_straight,
            ) = state_key
            # if current_cost > best_so_far:
            #     continue

            seen[state_key] = current_cost
            if current_pos == Point(grid.w - 1, grid.h - 1):
                new_cost = current_cost + grid.at(current_pos)
                best_so_far = min(best_so_far, new_cost)
                seen[state_key] = best_so_far
                continue

            dirs = [current_dir.clockwise, current_dir.counter_clockwise]
            if current_steps_straight < 3:
                dirs.append(current_dir)

            for d in dirs:
                next_pos = current_pos.neighbor(d)
                next_cost = grid.get(next_pos)
                if not next_cost:
                    continue
                cost_so_far = current_cost + next_cost
                # if cost_so_far > best_so_far:
                #     continue
                # best_so_far = cost_so_far
                queue.append(
                    (
                        (
                            next_pos,
                            d,
                            1 if current_dir is not d else current_steps_straight + 1,
                        ),
                        cost_so_far,
                    )
                )
        return int(best_so_far)

    def _part2(self) -> Solution:
        raise NotImplementedError
