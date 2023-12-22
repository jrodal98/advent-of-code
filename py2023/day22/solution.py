#!/usr/bin/env python3
# www.jrodal.com


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


@dataclass(frozen=True)
class Brick:
    p1: Point3D
    p2: Point3D

    @classmethod
    def from_string(cls, s: str) -> "Brick":
        p1, p2 = s.split("~")
        return cls(
            Point3D.from_string(p1),
            Point3D.from_string(p2),
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

    def drop(self) -> "Brick":
        return Brick(
            Point3D(self.p1.x, self.p1.y, self.p1.z - 1),
            Point3D(self.p2.x, self.p2.y, self.p2.z - 1),
        )


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        return list(self._brick_fall_counts().values()).count(0)

    def _part2(self) -> Solution:
        return sum(self._brick_fall_counts().values())

    def _brick_fall_counts(self) -> dict[Brick, int]:
        bricks = [Brick.from_string(s) for s in self.data.splitlines()]
        bricks.sort()
        for i, brick in enumerate(bricks):
            while brick.p1.z > 1 and not any(
                brick.on_top_of_other_brick(b) for b in bricks[:i]
            ):
                brick = brick.drop()
            bricks[i] = brick

        brick_is_on_map = {}
        brick_supports_map = {}

        for i in range(len(bricks)):
            for j in range(len(bricks)):
                if i != j and bricks[i].on_top_of_other_brick(bricks[j]):
                    brick_is_on_map.setdefault(bricks[i], set()).add(bricks[j])
                    brick_supports_map.setdefault(bricks[j], set()).add(bricks[i])

        return {
            b: self._calc_bricks_that_would_fall(
                b, brick_is_on_map, brick_supports_map, set()
            )
            for b in bricks
        }

    def _calc_bricks_that_would_fall(
        self,
        brick: Brick,
        brick_is_on_map: dict[Brick, set[Brick]],
        brick_supports_map: dict[Brick, set[Brick]],
        fallen_bricks: set[Brick],
    ) -> int:
        fallen_bricks.add(brick)
        for b in brick_supports_map.get(brick, set()):
            if not brick_is_on_map[b] - fallen_bricks:
                self._calc_bricks_that_would_fall(
                    b, brick_is_on_map, brick_supports_map, fallen_bricks
                )
        return len(fallen_bricks) - 1
