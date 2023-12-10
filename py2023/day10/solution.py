#!/usr/bin/env python3
# www.jrodal.com

import networkx as nx

from enum import Enum
from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return max(
            nx.shortest_path_length(
                *self._get_graph_and_s_pos()
            ).values()  # pyright: ignore
        )

    def _part2(self) -> Solution:
        graph, _ = self._get_graph_and_s_pos()

        path = sorted(list(nx.simple_cycles(graph)), key=lambda s: len(s))[-1]

        shoelace = path + [path[0]]

        area = 0
        for a, b in zip(shoelace, shoelace[1:]):
            area += (a[0] * b[1]) - (a[1] * b[0])

        return int(area / 2 - len(path) / 2 + 1)

    def _get_graph_and_s_pos(self) -> tuple[nx.DiGraph, tuple[int, int]]:
        grid = Grid.from_lines(self.data)
        graph = nx.DiGraph()
        s_pos = grid.find_cell("S")
        self._replace_s(*s_pos, grid)
        for y in range(grid.h):
            for x in range(grid.w):
                for cx, cy in self._get_valid_transitions(grid, x, y):
                    graph.add_edge((x, y), (cx, cy))
        return graph, s_pos

    def _get_valid_transitions(
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

    def _is_valid_transition(
        self, possible_next: str | None, direction: Direction
    ) -> bool:
        possible_next = possible_next or "X"
        match direction:
            case Direction.LEFT:
                return possible_next in "L-F"
            case Direction.RIGHT:
                return possible_next in "-7J"
            case Direction.UP:
                return possible_next in "|F7"
            case Direction.DOWN:
                return possible_next in "|JL"
            case _:
                return False

    def _replace_s(self, x: int, y: int, grid: Grid) -> None:
        match self._is_valid_transition(
            grid.left(x, y), Direction.LEFT
        ), self._is_valid_transition(
            grid.right(x, y), Direction.RIGHT
        ), self._is_valid_transition(
            grid.up(x, y), Direction.UP
        ), self._is_valid_transition(
            grid.down(x, y), Direction.DOWN
        ):
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
