#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid, Point
import networkx as nx
from collections import deque

import sys

sys.setrecursionlimit(100000000)


def steps_to_end(grid: Grid[str], current_position: Point, path: set[Point]) -> int:
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


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return steps_to_end(self.grid, Point(1, 0), set())

    def _part2(self) -> Solution:
        junctions = {Point(1, 0), Point(self.grid.w - 2, self.grid.h - 1)}
        for source, v in self.grid.iter():
            if v == "#":
                continue
            num_valid_neighbors = 0
            for n in self.grid.neighbors(source):
                if n != "#":
                    num_valid_neighbors += 1
            if num_valid_neighbors > 2:
                junctions.add(source)

        graph = nx.DiGraph()
        for source in junctions:
            queue: deque[tuple[Point, int]] = deque([(source, 0)])
            seen = set()
            while queue:
                current_pos, dist = queue.popleft()
                if current_pos in seen:
                    continue
                seen.add(current_pos)
                if current_pos != source and current_pos in junctions:
                    graph.add_edge(source, current_pos, weight=dist)
                    continue
                for n, d in self.grid.neighbors_with_direction(current_pos):
                    if n != "#":
                        queue.append((current_pos.neighbor(d), dist + 1))

        all_paths = nx.all_simple_paths(
            graph, Point(1, 0), Point(self.grid.w - 2, self.grid.h - 1)
        )
        ans = 0
        for i, p in enumerate(all_paths):
            ans = max(ans, nx.path_weight(graph, p, weight="weight"))
            if i % 1000 == 0:
                print(ans)
        return ans
