#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Direction, Grid, Point


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

    v = grid.get(point)
    match v, direction:
        case None, _:
            return None
        case ".", _:
            return move_in_grid(
                grid, point.point_at_direction(direction), direction, visited_points
            )
        case "/", Direction.RIGHT:
            return move_in_grid(
                grid,
                point.point_at_direction(Direction.UP),
                Direction.UP,
                visited_points,
            )
        case "/", Direction.LEFT:
            return move_in_grid(
                grid,
                point.point_at_direction(Direction.DOWN),
                Direction.DOWN,
                visited_points,
            )
        case "/", Direction.UP:
            return move_in_grid(
                grid,
                point.point_at_direction(Direction.RIGHT),
                Direction.RIGHT,
                visited_points,
            )
        case "/", Direction.DOWN:
            return move_in_grid(
                grid,
                point.point_at_direction(Direction.LEFT),
                Direction.LEFT,
                visited_points,
            )
        case "\\", Direction.LEFT:
            return move_in_grid(
                grid,
                point.point_at_direction(Direction.UP),
                Direction.UP,
                visited_points,
            )
        case "\\", Direction.RIGHT:
            return move_in_grid(
                grid,
                point.point_at_direction(Direction.DOWN),
                Direction.DOWN,
                visited_points,
            )
        case "\\", Direction.DOWN:
            return move_in_grid(
                grid,
                point.point_at_direction(Direction.RIGHT),
                Direction.RIGHT,
                visited_points,
            )
        case "\\", Direction.UP:
            return move_in_grid(
                grid,
                point.point_at_direction(Direction.LEFT),
                Direction.LEFT,
                visited_points,
            )
        case "-", Direction.LEFT | Direction.RIGHT:
            return move_in_grid(
                grid,
                point.point_at_direction(direction),
                direction,
                visited_points,
            )
        case "|", Direction.UP | Direction.DOWN:
            return move_in_grid(
                grid,
                point.point_at_direction(direction),
                direction,
                visited_points,
            )
        case "|", Direction.LEFT | Direction.RIGHT:
            for d in (Direction.UP, Direction.DOWN):
                move_in_grid(
                    grid,
                    point.point_at_direction(d),
                    d,
                    visited_points,
                )
            return
        case "-", Direction.UP | Direction.DOWN:
            for d in (Direction.LEFT, Direction.RIGHT):
                move_in_grid(
                    grid,
                    point.point_at_direction(d),
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
        move_in_grid(grid, Point(0, 0), Direction.RIGHT, visited_points)
        return len(visited_points)

    def _part2(self) -> Solution:
        raise NotImplementedError
