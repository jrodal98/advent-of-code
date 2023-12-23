#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid, Point

import sys

sys.setrecursionlimit(100000000)


def steps_to_end(grid: Grid[str], current_position: Point, path: set[Point]) -> int:
    assert current_position not in path
    if current_position == Point(grid.w - 2, grid.h - 1):
        return 0
    path.add(current_position)
    tile = grid.at(current_position)

    match tile:
        case ">":
            possible_positions = [current_position.right]
        case "<":
            possible_positions = [current_position.left]
        case "^":
            possible_positions = [current_position.up]
        case "v":
            possible_positions = [current_position.down]
        case ".":
            possible_positions = [
                current_position.up,
                current_position.down,
                current_position.left,
                current_position.right,
            ]
        case "#":
            assert False, "Can't be here"
        case _:
            assert False, "wtf?"

    best_so_far = -100000000000000
    for new_position in possible_positions:
        if new_position not in path and grid.get(new_position, "#") != "#":
            best_so_far = max(
                best_so_far, 1 + steps_to_end(grid, new_position, path.copy())
            )
    return best_so_far


def steps_to_end_p2(
    grid: Grid[str], current_position: Point, visited: Grid[bool], steps: int = 0
) -> int:
    if current_position == Point(grid.w - 2, grid.h - 1):
        return steps

    possible_positions = [
        current_position.up,
        current_position.down,
        current_position.left,
        current_position.right,
    ]

    best_so_far = -100000000000000

    visited.replace(current_position, True)
    for new_position in possible_positions:
        if not visited.get(new_position, True) and grid.get(new_position, "#") != "#":
            best_so_far = max(
                best_so_far,
                steps_to_end_p2(grid, new_position, visited, steps + 1),
            )
    visited.replace(current_position, False)
    return best_so_far


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return steps_to_end(self.grid, Point(1, 0), set())

    def _part2(self) -> Solution:
        ans = steps_to_end_p2(
            self.grid, Point(1, 0), self.grid.transform(lambda x: False)
        )
        return ans
