#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Direction, Point
from collections import deque


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return self._compute(0, 3)

    def _part2(self) -> Solution:
        return self._compute(4, 10)

    def _compute(self, min_steps_forward: int, max_steps_forward: int) -> Solution:
        grid = self.grid.transform(lambda x: int(x))
        state = ((Point(0, 0), Direction.RIGHT, 0), 0)
        seen = {}
        seen_no_dir = {}
        queue = deque([state])
        best_so_far = 1000
        skipped = 0
        not_skipped = 0
        paths_found = 0
        i = 0
        while queue:
            i += 1
            state_key, current_cost = queue.pop()
            (
                current_pos,
                current_dir,
                current_steps_straight,
            ) = state_key
            if current_cost >= best_so_far:
                seen_no_dir[current_pos] = min(
                    current_cost, seen_no_dir.get(current_pos, 1000)
                )
                continue
            if state_key in seen and current_cost >= seen[state_key]:
                continue

            distance_to_finish = current_pos.manhattan_distance(
                Point(grid.w - 1, grid.h - 1)
            )

            if (
                current_pos in seen_no_dir
                and current_cost > seen_no_dir[current_pos] + 10
            ):
                seen[state_key] = 10000
                skipped += 1
                continue

            if current_pos == Point(grid.w - 1, grid.h - 1):
                paths_found += 1
                new_cost = current_cost
                best_so_far = min(best_so_far, new_cost)
                seen[state_key] = best_so_far
                continue

            factor = 1
            if distance_to_finish > 50:
                if 100 < current_cost < 200:
                    factor = 3
                elif 300 < current_cost < 600:
                    factor = 2

                if current_cost > 300 and distance_to_finish > 230:
                    factor = 10

            best_possible_score = current_cost + distance_to_finish * factor
            if best_possible_score > best_so_far:
                skipped += 1
                seen[state_key] = best_possible_score
                continue

            not_skipped += 1
            if i % 25000 == 0:
                print(
                    f"{len(queue)}, {paths_found=}, {best_so_far=}, {skipped=}, {not_skipped=}, {current_cost=}, {distance_to_finish=}"
                )

            seen[state_key] = current_cost
            seen_no_dir[current_pos] = min(
                current_cost, seen_no_dir.get(current_pos, 1000)
            )

            if current_steps_straight < min_steps_forward:
                dirs = [current_dir]
            else:
                dirs = [current_dir.clockwise, current_dir.counter_clockwise]
                if current_steps_straight < max_steps_forward:
                    dirs.append(current_dir)

            # this hacky bullshit is to make it such that I prefer moving
            # right and down so that I can reach an end state faster
            if Direction.DOWN in dirs:
                dirs.remove(Direction.DOWN)
                dirs.insert(0, Direction.DOWN)
            if Direction.RIGHT in dirs:
                dirs.remove(Direction.RIGHT)
                dirs.insert(0, Direction.RIGHT)

            for d in dirs:
                next_pos = current_pos.neighbor(d)
                next_cost = grid.get(next_pos)
                if not next_cost:
                    continue
                cost_so_far = current_cost + next_cost
                queue.append(
                    (  # pyright: ignore
                        (
                            next_pos,
                            d,
                            1 if current_dir is not d else current_steps_straight + 1,
                        ),
                        cost_so_far,
                    )
                )
        return int(best_so_far)
