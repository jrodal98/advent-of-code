#!/usr/bin/env python3
# www.jrodal.com

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
        g = Grid(data=["."] * w * h, w=w, h=h)
        self._set_animation_grid(g)
        robots = []
        for line in self.lines():
            px, py, vx, vy = ints(line, include_sign=True)
            robots.append((px, py, vx, vy))
            g.replace(Point(px, py), "#")

        for i in range(1, 1000000000000000):
            new_bots = []
            new_pos = set()
            all_x = [0] * w
            for robot in robots:
                old_x, old_y, vx, vy = robot
                new_x, new_y = (old_x + vx) % w, (old_y + vy) % h
                all_x[new_x] += 1
                new_bots.append((new_x, new_y, vx, vy))
                new_pos.add(Point(new_x, new_y))
            max_x = max(all_x)
            if max_x > 30:
                for x in range(g.w):
                    for y in range(g.h):
                        p = Point(x, y)
                        if p in new_pos:
                            g.replace(p, "#")
                        else:
                            g.replace(p, ".")
                self._update_animation(message=f"Time: {i}")
            robots = new_bots
            all_x = [0] * w
        assert False
