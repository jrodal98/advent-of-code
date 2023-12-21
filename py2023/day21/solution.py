#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from collections import deque


class Solver(BaseSolver):
    def _part1(self) -> Solution:
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
            if steps_taken == 64:
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
        raise NotImplementedError
