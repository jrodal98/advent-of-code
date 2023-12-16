#!/usr/bin/env python3
# www.jrodal.com

import networkx as nx

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Direction, Grid, Point


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
            area += (a.x * b.y) - (a.y * b.x)
        return int(area / 2 - len(path) / 2 + 1)

    def _get_graph_and_s_pos(self) -> tuple[nx.DiGraph, Point]:
        grid = Grid.from_lines(self.data)
        graph = nx.DiGraph()
        s_pos = grid.find_cell("S")
        self._replace_s(s_pos, grid)
        for p1, _ in grid.iter():
            for p2 in self._get_valid_transitions(grid, p1):
                graph.add_edge(p1, p2)
        return graph, s_pos

    def _get_valid_transitions(self, grid: Grid, coord: Point) -> list[Point]:
        transitions = []
        for c, d in coord.neighbors_with_direction():
            if self._is_valid_transition(grid.get(c), d):
                transitions.append(c)

        return [p for p in transitions if grid.get(p)]

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

    def _replace_s(self, p: Point, grid: Grid) -> None:
        match self._is_valid_transition(
            grid.left(p), Direction.LEFT
        ), self._is_valid_transition(
            grid.right(p), Direction.RIGHT
        ), self._is_valid_transition(
            grid.up(p), Direction.UP
        ), self._is_valid_transition(
            grid.down(p), Direction.DOWN
        ):
            case True, True, False, False:
                grid.replace(p, value="-")
            case True, False, True, False:
                grid.replace(p, value="J")
            case True, False, False, True:
                grid.replace(p, value="7")
            case False, True, True, False:
                grid.replace(p, value="L")
            case False, True, False, True:
                grid.replace(p, value="F")
            case False, False, True, True:
                grid.replace(p, value="|")
            case _:
                assert False, "This shouldn't be possible"
