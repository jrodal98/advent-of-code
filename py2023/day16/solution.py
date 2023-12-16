#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Direction, Grid, Point

import sys

sys.setrecursionlimit(10000)


def move_in_grid(
    grid: Grid,
    point: Point | None,
    direction: Direction,
    visited_points: set[tuple[Point, Direction]],
) -> None:
    if not point:
        return None

    hk = (point, direction)
    if hk in visited_points:
        return None
    visited_points.add(hk)

    p = point.point_at_direction(direction)
    v = grid.get(p)
    match v, direction:
        case None, _:
            return None
        case ".", _:
            return move_in_grid(grid, p, direction, visited_points)
        case "/", Direction.RIGHT:
            return move_in_grid(
                grid,
                p,
                Direction.UP,
                visited_points,
            )
        case "/", Direction.LEFT:
            return move_in_grid(
                grid,
                p,
                Direction.DOWN,
                visited_points,
            )
        case "/", Direction.UP:
            return move_in_grid(
                grid,
                p,
                Direction.RIGHT,
                visited_points,
            )
        case "/", Direction.DOWN:
            return move_in_grid(
                grid,
                p,
                Direction.LEFT,
                visited_points,
            )
        case "\\", Direction.LEFT:
            return move_in_grid(
                grid,
                p,
                Direction.UP,
                visited_points,
            )
        case "\\", Direction.RIGHT:
            return move_in_grid(
                grid,
                p,
                Direction.DOWN,
                visited_points,
            )
        case "\\", Direction.DOWN:
            return move_in_grid(
                grid,
                p,
                Direction.RIGHT,
                visited_points,
            )
        case "\\", Direction.UP:
            return move_in_grid(
                grid,
                p,
                Direction.LEFT,
                visited_points,
            )
        case "-", Direction.LEFT | Direction.RIGHT:
            return move_in_grid(
                grid,
                p,
                direction,
                visited_points,
            )
        case "|", Direction.UP | Direction.DOWN:
            return move_in_grid(
                grid,
                p,
                direction,
                visited_points,
            )
        case "|", Direction.LEFT | Direction.RIGHT:
            for d in (Direction.UP, Direction.DOWN):
                move_in_grid(
                    grid,
                    p,
                    d,
                    visited_points,
                )
            return
        case "-", Direction.UP | Direction.DOWN:
            for d in (Direction.LEFT, Direction.RIGHT):
                move_in_grid(
                    grid,
                    p,
                    d,
                    visited_points,
                )
        case _, _:
            grid.display()
            print(point)
            assert False, f"{v=}, {direction=}"


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        grid = Grid.from_lines(self.data)
        visited_points = set()
        move_in_grid(grid, Point(-1, 0), Direction.RIGHT, visited_points)
        only_points = set()
        for p, _ in visited_points:
            only_points.add(p)
        only_points.remove(Point(-1, 0))
        return len(only_points)

    def _part2(self) -> Solution:
        grid = Grid.from_lines(self.data)
        boundary_points = set()
        for i in range(grid.h):
            boundary_points.add((Point(-1, i), Direction.RIGHT))
            boundary_points.add((Point(grid.w, i), Direction.LEFT))
        for j in range(grid.w):
            boundary_points.add((Point(j, -1), Direction.DOWN))
            boundary_points.add((Point(j, grid.h), Direction.UP))

        ans = 0
        for start_point, d in boundary_points:
            visited_points = set()
            move_in_grid(grid, start_point, d, visited_points)
            only_points = set()
            for p, _ in visited_points:
                only_points.add(p)
            only_points.remove(start_point)
            ans = max(ans, len(only_points))
        return ans
