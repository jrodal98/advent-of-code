#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Direction, Point
from collections import deque


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        grid = self.grid.transform(lambda x: int(x))
        self._set_animation_grid(self.grid)
        state = ((Point(0, 0), Direction.RIGHT, 0), 0)
        seen = {}
        seen_no_dir = {}
        queue = deque([state])
        best_so_far = 927
        skipped = 0
        not_skipped = 0
        paths_found = 0
        i = 0
        while queue:
            i += 1
            # state_key, current_cost = queue.popleft()
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

            self._update_animation(point=current_pos, refresh=len(queue) % 500 == 0)

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
            # elif current_cost < 600:
            #     factor = 2

            best_possible_score = current_cost + distance_to_finish * factor
            if best_possible_score > best_so_far:
                # best_so_far = possible_score
                skipped += 1
                seen[state_key] = best_possible_score
                continue
            else:
                # print("Possible score: ", best_possible_score)
                pass

            not_skipped += 1
            if i % 10000 == 0:
                print(
                    f"{len(queue)}, {paths_found=}, {best_so_far=}, {skipped=}, {not_skipped=}, {current_cost=}, {distance_to_finish=}"
                )

            seen[state_key] = current_cost
            seen_no_dir[current_pos] = min(
                current_cost, seen_no_dir.get(current_pos, 1000)
            )

            dirs = [current_dir.clockwise, current_dir.counter_clockwise]
            if current_steps_straight < 3:
                dirs.append(current_dir)

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

    def _part2(self) -> Solution:
        raise NotImplementedError
