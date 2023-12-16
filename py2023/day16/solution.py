#!/usr/bin/env python3
# www.jrodal.com

from copy import deepcopy
from collections import deque
from typing import Iterable
from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Direction, Grid, Point

from mpire import WorkerPool


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        self._set_animation_grid(grid=deepcopy(self.grid))
        return self._shoot_light_into_grid(self.grid, Point(-1, 0), Direction.RIGHT)

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
        return max(results)

    def _shoot_light_into_grid(
        self,
        grid: Grid,
        start_position: Point | None,
        start_direction: Direction,
    ) -> int:
        seen_states = set()
        queue = deque([(start_position, start_direction)])
        while queue:
            current_state = queue.popleft()
            current_position, current_direction = current_state
            if not current_position:
                continue
            if current_state in seen_states:
                continue

            self._update_animation(
                point=current_position,
                value="#",
                message=f"current_state={current_state}",
            )
            seen_states.add(current_state)

            new_position = current_position.neighbor(current_direction)
            obstacle = grid.get(new_position)
            for new_direction in self._bounce_beam(obstacle, current_direction):
                queue.append((new_position, new_direction))

        return len({p for p, _ in seen_states}) - 1

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
