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
    _WALLS: set[str] = {"L", "-", "F", "7", "|", "J"}

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

    def _part1(self) -> Solution:
        grid = Grid.from_lines(self.data, delimiter="")
        graph = nx.DiGraph()
        for y, row in enumerate(grid.rows):
            for x, c in enumerate(row):
                identifier = f"{x}-{y}"
                for cx, cy in self.get_valid_transitions(grid, x, y, False):
                    graph.add_edge(identifier, f"{cx}-{cy}")

        x, y = grid.find_cell("S")
        return max(
            nx.shortest_path_length(graph, f"{x}-{y}").values()  # pyright: ignore
        )

    def get_valid_transitions(
        self, grid: Grid, x: int, y: int, escape: bool = False
    ) -> list[tuple[int, int]]:
        transitions = []
        for coord, d in [
            (grid.left_coord(x, y), Direction.LEFT),
            (grid.right_coord(x, y), Direction.RIGHT),
            (grid.up_coord(x, y), Direction.UP),
            (grid.down_coord(x, y), Direction.DOWN),
        ]:
            if self._is_valid_transition(grid.get(*coord), d, escape):
                transitions.append(coord)

        if not escape:
            return transitions

        left, right, up, down = (
            grid.left(x, y),
            grid.right(x, y),
            grid.up(x, y),
            grid.down(x, y),
        )

        if left in self._WALLS and up in self._WALLS:
            transitions.append(grid.upper_left_coord(x, y))

        if right in self._WALLS and up in self._WALLS:
            transitions.append(grid.upper_right_coord(x, y))

        if left in self._WALLS and down in self._WALLS:
            transitions.append(grid.bottom_left_coord(x, y))

        if right in self._WALLS and down in self._WALLS:
            transitions.append(grid.bottom_right_coord(x, y))

        return transitions

    def _part2(self) -> Solution:
        grid = Grid.from_lines(self.data, delimiter="", padding=".")
        graph = nx.DiGraph()
        for y, row in enumerate(grid.rows):
            for x, c in enumerate(row):
                identifier = f"{x}-{y}"
                for cx, cy in self.get_valid_transitions(grid, x, y, True):
                    graph.add_edge(identifier, f"{cx}-{cy}")

        print(set(nx.nodes(graph)) - set(nx.dfs_postorder_nodes(graph, "0-0")))
        assert False
