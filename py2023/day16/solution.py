#!/usr/bin/env python3
# www.jrodal.com

from typing import Iterable
from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Direction, Grid, Point

import sys

sys.setrecursionlimit(10000)


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        grid = Grid.from_lines(self.data)
        seen_states = set()
        self._move_in_grid(grid, Point(-1, 0), Direction.RIGHT, seen_states)
        return len({p for p, _ in seen_states}) - 1

    def _part2(self) -> Solution:
        grid = Grid.from_lines(self.data)
        boundary_states = set()
        for i in range(grid.h):
            boundary_states.add((Point(-1, i), Direction.RIGHT))
            boundary_states.add((Point(grid.w, i), Direction.LEFT))
        for j in range(grid.w):
            boundary_states.add((Point(j, -1), Direction.DOWN))
            boundary_states.add((Point(j, grid.h), Direction.UP))

        ans = 0
        for start_point, d in boundary_states:
            seen_states = set()
            self._move_in_grid(grid, start_point, d, seen_states)
            ans = max(ans, len({p for p, _ in seen_states}))
        return ans - 1

    def _move_in_grid(
        self,
        grid: Grid,
        current_position: Point | None,
        direction: Direction,
        seen_states: set[tuple[Point, Direction]],
    ) -> None:
        if not current_position:
            return None

        hashkey = (current_position, direction)
        if hashkey in seen_states:
            return None
        seen_states.add(hashkey)

        neighbor = current_position.point_at_direction(direction)
        neighbor_value = grid.get(neighbor)
        for d in self._bounce_beam(neighbor_value, direction):
            self._move_in_grid(grid, neighbor, d, seen_states)

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
