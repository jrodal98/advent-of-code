#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from collections import deque


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        if self._is_unit_test:
            target_steps = 6
        else:
            target_steps = 64
        visited = set()
        visited_at_six = set()
        places_to_go = deque([(self.grid.find("S"), 0)])
        while places_to_go:
            if not places_to_go:
                break
            current_place, steps_taken = places_to_go.popleft()
            if (current_place, steps_taken) in visited:
                continue
            visited.add((current_place, steps_taken))
            if steps_taken == target_steps:
                visited_at_six.add(current_place)
                continue

            for neighbor, direction in self.grid.neighbors_with_direction(
                current_place
            ):
                if neighbor in (".", "S"):
                    places_to_go.append(
                        (
                            current_place.neighbor(direction),
                            steps_taken + 1,  # pyright: ignore
                        )
                    )
        return len(visited_at_six)

    def _part2(self) -> Solution:
        if self._is_unit_test:
            target_steps = 100
        else:
            target_steps = 26501365
        visited = set()
        visited_at_six = set()
        places_to_go = deque([(self.grid.find("S"), 0)])
        while places_to_go:
            if not places_to_go:
                break
            current_place, steps_taken = places_to_go.popleft()
            if (current_place, steps_taken) in visited:
                continue
            visited.add((current_place, steps_taken))
            if steps_taken == target_steps:
                visited_at_six.add(current_place)
                continue

            # TODO: need to add the "allow_overflow" logic to neighbors
            for _, direction in self.grid.neighbors_with_direction(
                current_place, disqualify="#", allow_overflow=True
            ):
                places_to_go.append(
                    (
                        current_place.neighbor(direction),
                        steps_taken + 1,  # pyright: ignore
                    )
                )
        if self._is_unit_test:
            return len(visited_at_six)

        return 0
