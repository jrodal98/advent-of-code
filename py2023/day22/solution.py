#!/usr/bin/env python3
# www.jrodal.com

from typing import Iterator

from rich.progress import track

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
        return self.p1.z < other.p1.z

    #     1,0,1~1,2,1   <- A
    #     0,0,2~2,0,2   <- B
    #     0,2,3~2,2,3   <- C

    def on_top_of_other_brick(self, other: "Brick") -> bool:
        # xs1,ys1,zs1 = self.start
        # xe1,ye1,ze1 = self.end
        # xs2,ys2,zs2 = other.start
        # xe2,ye2,ze2 = other.end

        # return (xs1<=xe2 and xs2<=xe1 and
        #         ys1<=ye2 and ys2<=ye1 and
        #         zs1<=ze2 and zs2<=ze1)
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

        ans = 0
        for i in track(range(len(bricks))):
            bricks_to_check = bricks[:i] + bricks[i + 1 :]
            fell = False
            for j, brick in enumerate(bricks_to_check):
                if brick.p1.z > 1 and not any(
                    brick.on_top_of_other_brick(b) for b in bricks_to_check[:j]
                ):
                    fell = True
                    break
            if not fell:
                ans += 1

        return ans

    def _part2(self) -> Solution:
        raise NotImplementedError
