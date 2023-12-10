#!/usr/bin/env python3
# www.jrodal.com

import networkx as nx

from enum import Enum
from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid


"""
.....
.S-7.
.|.|.
.L-J.
.....
"""


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    UPPER_LEFT = 4
    UPPER_RIGHT = 5
    LOWER_LEFT = 6
    LOWER_RIGHT = 7


class Solver(BaseSolver):
    def _is_valid_transition(
        self, possible_next: str | None, direction: Direction, escape: bool = False
    ) -> bool:
        if escape and possible_next == ".":
            return True
        match possible_next, direction:
            case None, _:
                return False
            case "L" | "-" | "F", Direction.LEFT:
                return True
            case "-" | "7" | "J", Direction.RIGHT:
                return True
            case "|" | "F" | "7", Direction.UP:
                return True
            case "|" | "J" | "L", Direction.DOWN:
                return True
            case _, _:
                return False

    def replace_s(self, x: int, y: int, grid: Grid) -> None:
        left = self._is_valid_transition(grid.left(x, y), Direction.LEFT)
        right = self._is_valid_transition(grid.right(x, y), Direction.RIGHT)
        up = self._is_valid_transition(grid.up(x, y), Direction.UP)
        down = self._is_valid_transition(grid.down(x, y), Direction.DOWN)

        match left, right, up, down:
            case True, True, False, False:
                grid.replace(x, y, "-")
            case True, False, True, False:
                grid.replace(x, y, "J")
            case True, False, False, True:
                grid.replace(x, y, "7")
            case False, True, True, False:
                grid.replace(x, y, "L")
            case False, True, False, True:
                grid.replace(x, y, "F")
            case False, False, True, True:
                grid.replace(x, y, "|")
            case _:
                assert False, "This shouldn't be possible"

    def _part1(self) -> Solution:
        grid = Grid.from_lines(self.data, delimiter="")
        s_pos = grid.find_cell("S")
        self.replace_s(*s_pos, grid)
        graph = nx.DiGraph()
        for y in range(grid.h):
            for x in range(grid.w):
                for cx, cy in self.get_valid_transitions(grid, x, y):
                    graph.add_edge((x, y), (cx, cy))

        a = sorted(list(nx.simple_cycles(graph)), key=lambda s: len(s))[-1]
        return len(a) // 2
        # return max(nx.shortest_path_length(graph, s_pos).values())  # pyright: ignore

    def get_valid_transitions(
        self, grid: Grid, x: int, y: int
    ) -> list[tuple[int, int]]:
        transitions = []
        for coord, d in [
            (grid.left_coord(x, y), Direction.LEFT),
            (grid.right_coord(x, y), Direction.RIGHT),
            (grid.up_coord(x, y), Direction.UP),
            (grid.down_coord(x, y), Direction.DOWN),
        ]:
            if self._is_valid_transition(grid.get(*coord), d):
                transitions.append(coord)

        return [(x, y) for x, y in transitions if grid.get(x, y)]

    def _part2(self) -> Solution:
        grid = Grid.from_lines(self.data, delimiter="")
        s_pos = grid.find_cell("S")
        self.replace_s(*s_pos, grid)
        graph = nx.DiGraph()
        for y in range(grid.h):
            for x in range(grid.w):
                for cx, cy in self.get_valid_transitions(grid, x, y):
                    graph.add_edge((x, y), (cx, cy))

        path = sorted(list(nx.simple_cycles(graph)), key=lambda s: len(s))[-1]

        shoelace = path + [path[0]]

        area = 0
        for a, b in zip(shoelace, shoelace[1:]):
            area += (a[0] * b[1]) - (a[1] * b[0])

        return int(area / 2 - len(path) / 2 + 1)
