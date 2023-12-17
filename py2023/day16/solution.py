#!/usr/bin/env python3
# www.jrodal.com

from collections import deque
from typing import Iterable
from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Direction, Grid, Point

from mpire import WorkerPool


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        self._set_animation_grid(grid=self.grid.copy())
        return self._shoot_light_into_grid(self.grid, Point(-1, 0), Direction.RIGHT)[2]

    def _part2(self) -> Solution:
        boundary_states = set()
        for i in range(self.grid.h):
            boundary_states.add((Point(-1, i), Direction.RIGHT))
            boundary_states.add((Point(self.grid.w, i), Direction.LEFT))
        for j in range(self.grid.w):
            boundary_states.add((Point(j, -1), Direction.DOWN))
            boundary_states.add((Point(j, self.grid.h), Direction.UP))

        with WorkerPool(n_jobs=8, shared_objects=self.grid) as pool:
            results = pool.map(
                self._shoot_light_into_grid, boundary_states, progress_bar=True
            )
        best = max(results, key=lambda x: x[2])
        if self._animate:
            self._set_animation_grid(grid=self.grid.copy())
            self._shoot_light_into_grid(self.grid, best[0], best[1])[2]
        return best[2]

    def _shoot_light_into_grid(
        self,
        grid: Grid,
        start_position: Point,
        start_direction: Direction,
    ) -> tuple[Point | None, Direction, int]:
        seen_states = set()
        unique_positions = set()
        queue = deque([(start_position, start_direction)])
        while queue:
            current_state = queue.popleft()
            current_position, current_direction = current_state
            if not current_position:
                continue
            if current_state in seen_states:
                continue

            seen_states.add(current_state)
            unique_positions.add(current_position)

            new_position = current_position.neighbor(current_direction)
            self._update_animation(
                point=current_position,
                value=current_direction.arrow,
                message=f"{current_state}, energized: {len(unique_positions) - 1} num_active_rays: {len(queue) + 1}",
                points_to_colors={
                    start_position: "blue",
                    current_position: "green",
                    new_position: "red",
                },
                values_to_colors={
                    "\\": "cyan",
                    "-": "cyan",
                    "|": "cyan",
                    "/": "cyan",
                    ".": "black",
                },
                refresh=grid.h < 15 or len(seen_states) % 50 == 1,
            )
            obstacle = grid.get(new_position)
            for new_direction in self._bounce_beam(obstacle, current_direction):
                queue.append((new_position, new_direction))

        return (start_position, start_direction, len(unique_positions) - 1)

    def _bounce_beam(
        self, obstacle: str | None, current_direction: Direction
    ) -> Iterable[Direction]:
        match obstacle, current_direction:
            case "/", Direction.RIGHT | Direction.LEFT:
                return [current_direction.counter_clockwise]
            case "/", Direction.UP | Direction.DOWN:
                return [current_direction.clockwise]
            case "\\", Direction.RIGHT | Direction.LEFT:
                return [current_direction.clockwise]
            case "\\", Direction.UP | Direction.DOWN:
                return [current_direction.counter_clockwise]
            case "-", Direction.UP | Direction.DOWN:
                return [Direction.LEFT, Direction.RIGHT]
            case "|", Direction.RIGHT | Direction.LEFT:
                return [Direction.UP, Direction.DOWN]
            case None, _:
                return []
            case _, _:
                return [current_direction]
