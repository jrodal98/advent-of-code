#!/usr/bin/env python3
# www.jrodal.com

from typing import Iterator


from aoc_utils.base_solver import BaseSolver, Solution
from dataclasses import dataclass


@dataclass(frozen=True)
class Point3D:
    x: int
    y: int
    z: int

    @classmethod
    def from_string(cls, s: str) -> "Point3D":
        x, y, z = s.split(",")
        return cls(int(x), int(y), int(z))


def get_identifier() -> Iterator[str]:
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        yield c


IDENTIFIERS = get_identifier()


@dataclass(frozen=True)
class Brick:
    p1: Point3D
    p2: Point3D
    identifier: str = "unknown"

    @classmethod
    def from_string(cls, s: str) -> "Brick":
        p1, p2 = s.split("~")
        return cls(
            Point3D.from_string(p1),
            Point3D.from_string(p2),
            next(IDENTIFIERS, "unknown"),
        )

    def __lt__(self, other: "Brick") -> bool:
        return max(self.p1.z, self.p2.z) < max(other.p1.z, other.p2.z)

    def on_top_of_other_brick(self, other: "Brick") -> bool:
        return (
            self.p1.z == other.p2.z + 1
            and self.p1.x <= other.p2.x
            and other.p1.x <= self.p2.x
            and self.p1.y <= other.p2.y
            and other.p1.y <= self.p2.y
        )


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        bricks = [Brick.from_string(s) for s in self.data.splitlines()]
        bricks.sort()
        for i, brick in enumerate(bricks):
            while brick.p1.z > 1 and not any(
                brick.on_top_of_other_brick(b) for b in bricks[:i]
            ):
                brick = Brick(
                    Point3D(brick.p1.x, brick.p1.y, brick.p1.z - 1),
                    Point3D(brick.p2.x, brick.p2.y, brick.p2.z - 1),
                    brick.identifier,
                )
            bricks[i] = brick

        brick_is_on_map = {}
        brick_supports_map = {}

        for i in range(len(bricks)):
            for j in range(len(bricks)):
                if i != j and bricks[i].on_top_of_other_brick(bricks[j]):
                    brick_is_on_map.setdefault(bricks[i], []).append(bricks[j])
                    brick_supports_map.setdefault(bricks[j], []).append(bricks[i])

        ans = 0
        for brick in bricks:
            bricks_it_supports = brick_supports_map.get(brick, [])
            can_disintegrate = True
            for b in bricks_it_supports:
                if len(brick_is_on_map[b]) == 1:
                    can_disintegrate = False
                    break
            ans += int(can_disintegrate)

        return ans

    def _part2(self) -> Solution:
        bricks = [Brick.from_string(s) for s in self.data.splitlines()]
        bricks.sort()
        for i, brick in enumerate(bricks):
            while brick.p1.z > 1 and not any(
                brick.on_top_of_other_brick(b) for b in bricks[:i]
            ):
                brick = Brick(
                    Point3D(brick.p1.x, brick.p1.y, brick.p1.z - 1),
                    Point3D(brick.p2.x, brick.p2.y, brick.p2.z - 1),
                    brick.identifier,
                )
            bricks[i] = brick

        brick_is_on_map = {}
        brick_supports_map = {}

        for i in range(len(bricks)):
            for j in range(len(bricks)):
                if i != j and bricks[i].on_top_of_other_brick(bricks[j]):
                    brick_is_on_map.setdefault(bricks[i], set()).add(bricks[j])
                    brick_supports_map.setdefault(bricks[j], set()).add(bricks[i])

        bricks.sort(reverse=True)

        return sum(
            calc_bricks_that_would_fall(b, brick_is_on_map, brick_supports_map, set())
            for b in bricks
        )


def calc_bricks_that_would_fall(
    brick: Brick,
    brick_is_on_map,
    brick_supports_map,
    fallen_bricks,
) -> int:
    fallen_bricks.add(brick)
    bricks_it_supports = brick_supports_map.get(brick, set())
    for b in bricks_it_supports:
        if not brick_is_on_map[b] - fallen_bricks:
            calc_bricks_that_would_fall(
                b, brick_is_on_map, brick_supports_map, fallen_bricks
            )
    return len(fallen_bricks) - 1
