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


class Solver(BaseSolver):
    def _is_valid_transition(
        self, possible_next: str | None, direction: Direction
    ) -> bool:
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
                left, right, up, down = (
                    grid.left(x, y),
                    grid.right(x, y),
                    grid.up(x, y),
                    grid.down(x, y),
                )

                if c == "S":
                    identifier = c
                else:
                    identifier = f"{x}-{y}"

                if self._is_valid_transition(left, Direction.LEFT):
                    cx, cy = grid.left_coord(x, y)
                    graph.add_edge(identifier, f"{cx}-{cy}")

                if self._is_valid_transition(right, Direction.RIGHT):
                    cx, cy = grid.right_coord(x, y)
                    graph.add_edge(identifier, f"{cx}-{cy}")

                if self._is_valid_transition(up, Direction.UP):
                    cx, cy = grid.up_coord(x, y)
                    graph.add_edge(identifier, f"{cx}-{cy}")

                if self._is_valid_transition(down, Direction.DOWN):
                    cx, cy = grid.down_coord(x, y)
                    graph.add_edge(identifier, f"{cx}-{cy}")

        return max(nx.shortest_path_length(graph, "S").values())  # pyright: ignore

    def _part2(self) -> Solution:
        raise NotImplementedError
