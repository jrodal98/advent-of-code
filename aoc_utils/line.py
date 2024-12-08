#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.point import Point
from dataclasses import dataclass

from enum import Enum, auto
from typing import Callable, Iterator


class PointIterStrategy(Enum):
    ALTERNATE = auto()
    FROM_P1 = auto()
    FROM_P2 = auto()


@dataclass(frozen=True)
class Line:
    p1: Point
    p2: Point

    @property
    def dx(self) -> int:
        return self.p1.x - self.p2.x

    @property
    def dy(self) -> int:
        return self.p1.y - self.p2.y

    @property
    def dxdy(self) -> Point:
        return Point(self.dx, self.dy)

    def iter(
        self,
        *,
        exclude_start: bool = False,
        strategy=PointIterStrategy.ALTERNATE,
        continue_while: Callable[[Point], bool] = lambda _: True,
        stop_if: Callable[[Point], bool] = lambda _: False,
        max_steps: int | None = None,
    ) -> Iterator[Point]:
        if not exclude_start:
            yield self.p1
            yield self.p2

        p1 = self.p1 if strategy is not PointIterStrategy.FROM_P2 else None
        p2 = self.p2 if strategy is not PointIterStrategy.FROM_P1 else None
        steps = 0
        while (p1 or p2) and (max_steps is None or steps < max_steps):
            steps += 1
            if p1:
                p1 += self.dxdy
                if stop_if(p1) or not continue_while(p1):
                    p1 = None
                else:
                    yield p1
            if p2:
                p2 -= self.dxdy
                if stop_if(p2) or not continue_while(p2):
                    p2 = None
                else:
                    yield p2
