#!/usr/bin/env python3
# www.jrodal.com

from collections import defaultdict
from aoc_utils.helpers import ints
from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.grid import Grid
from aoc_utils.point import Point


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        if self._is_unit_test:
            w = 11
            h = 7
        else:
            w = 101
            h = 103

        time = 100

        g = Grid(data=[0] * w * h, w=w, h=h, allow_overflow=True)
        for line in self.lines():
            px, py, vx, vy = ints(line, include_sign=True)
            x = px + vx * time
            y = py + vy * time
            g[Point(x, y)] += 1

        mid_x, mid_y = w // 2, h // 2
        score = 1
        for lx, ux, ly, uy in [
            (0, mid_x, 0, mid_y),
            (0, mid_x, mid_y + 1, h),
            (mid_x + 1, w, 0, mid_y),
            (mid_x + 1, w, mid_y + 1, h),
        ]:
            q = 0
            for x in range(lx, ux):
                for y in range(ly, uy):
                    q += g.at(Point(x, y))
            score *= q
        return score

    def _part2(self) -> Solution:
        w = 101
        h = 103
        points_to_robots = defaultdict(set)
        self._set_animation_grid(Grid(data=["."] * w * h, w=w, h=h))
        for line in self.lines():
            px, py, vx, vy = ints(line, include_sign=True)
            points_to_robots[(px, py)].add((vx, vy))

        for i in range(1, 1000000000000000):
            new_points_to_robots = defaultdict(set)
            unique_x_values = [0] * w
            for (px, py), robots in points_to_robots.items():
                for vx, vy in robots:
                    new_x, new_y = (px + vx) % w, (py + vy) % h
                    new_points_to_robots[(new_x, new_y)].add((vx, vy))
                    unique_x_values[new_x] += 1
            points_to_robots = new_points_to_robots
            # the logic below is how I actually solved the puzzle
            if self._animate and max(unique_x_values) > 30:
                for x, y in points_to_robots.keys():
                    self._update_animation(point=Point(x, y), value="#", refresh=False)
                self._update_animation(message=f"Step {i}")
                for x, y in points_to_robots.keys():
                    self._update_animation(point=Point(x, y), value=".", refresh=False)

            # This magic tricks gives the answer (the tree appears when no two robots overlap)
            if len(max(points_to_robots.values(), key=len)) == 1:
                return i
        assert False
