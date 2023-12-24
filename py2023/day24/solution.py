#!/usr/bin/env python3
# www.jrodal.com

from dataclasses import dataclass
from aoc_utils.base_solver import BaseSolver, Solution

from itertools import combinations
import z3


@dataclass
class Line:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int

    @property
    def slope(self) -> float:
        return self.vy / self.vx

    @property
    def y_intercept(self) -> float:
        return self.y - self.slope * self.x

    def intersect(self, other: "Line") -> tuple[float, float]:
        x = (other.y_intercept - self.y_intercept) / (self.slope - other.slope)
        y = self.slope * x + self.y_intercept
        return x, y


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        lines = []
        for line in self.data.splitlines():
            position_str, velocity_str = line.split(" @ ")
            x, y, z = position_str.split(", ")
            x, y, z = int(x), int(y), int(z)
            vx, vy, vz = velocity_str.split(", ")
            vx, vy, vz = int(vx), int(vy), int(vz)
            lines.append(Line(x, y, z, vx, vy, vz))

        if self._is_unit_test:
            min_xy = 7
            max_xy = 27
        else:
            min_xy = 200000000000000
            max_xy = 400000000000000

        ans = 0
        for line1, line2 in combinations(lines, 2):
            try:
                x, y = line1.intersect(line2)
                if (
                    min_xy <= x <= max_xy
                    and min_xy <= y <= max_xy
                    and (
                        (
                            (x > line1.x and line1.vx > 0)
                            or (x < line1.x and line1.vx < 0)
                        )
                        and (
                            (y > line1.y and line1.vy > 0)
                            or (y < line1.y and line1.vy < 0)
                        )
                    )
                    and (
                        (
                            (x > line2.x and line2.vx > 0)
                            or (x < line2.x and line2.vx < 0)
                        )
                        and (
                            (y > line2.y and line2.vy > 0)
                            or (y < line2.y and line2.vy < 0)
                        )
                    )
                ):
                    ans += 1
            except Exception:
                continue
        return ans

    def _part2(self) -> Solution:
        lines = []
        for line in self.data.splitlines():
            position_str, velocity_str = line.split(" @ ")
            x, y, z = position_str.split(", ")
            x, y, z = int(x), int(y), int(z)
            vx, vy, vz = velocity_str.split(", ")
            vx, vy, vz = int(vx), int(vy), int(vz)
            lines.append(Line(x, y, z, vx, vy, vz))

        # shamelessly stolen from https://github.com/mebeim/aoc/blob/master/2023/original_solutions/day24.py
        x, y, z, vx, vy, vz = (
            z3.Int("x"),
            z3.Int("y"),
            z3.Int("z"),
            z3.Int("vx"),
            z3.Int("vy"),
            z3.Int("vz"),
        )
        solver = z3.Solver()
        for i, line in enumerate(lines):
            t = z3.Int(f"T{i}")
            solver.add(t >= 0)
            solver.add(x + vx * t == line.x + line.vx * t)
            solver.add(y + vy * t == line.y + line.vy * t)
            solver.add(z + vz * t == line.z + line.vz * t)
        assert solver.check() == z3.sat
        model = solver.model()
        ans = model.eval(x + y + z)
        return int(str(ans))
