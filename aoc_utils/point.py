from __future__ import annotations

from dataclasses import astuple, dataclass
from enum import Enum
from math import sqrt
from typing import Iterable, Iterator


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    UPPER_LEFT = 4
    UPPER_RIGHT = 5
    LOWER_LEFT = 6
    LOWER_RIGHT = 7

    def __lt__(self, other: Direction) -> bool:
        return self.value < other.value

    def __mul__(self, factor: int) -> Point:
        match self:
            case self.UP:
                return Point(0, -factor)
            case self.DOWN:
                return Point(0, factor)
            case self.LEFT:
                return Point(-factor, 0)
            case self.RIGHT:
                return Point(factor, 0)
            case self.UPPER_LEFT:
                return Point(-factor, -factor)
            case self.UPPER_RIGHT:
                return Point(factor, -factor)
            case self.LOWER_LEFT:
                return Point(-factor, factor)
            case self.LOWER_RIGHT:
                return Point(factor, factor)
            case _:
                raise ValueError(f"Invalid direction: {self}")

    def __rmul__(self, factor: int) -> Point:
        return self * factor

    @property
    def arrow(self) -> str:
        match self:
            case self.UP:
                return "↑"
            case self.DOWN:
                return "↓"
            case self.LEFT:
                return "←"
            case self.RIGHT:
                return "→"
            case self.UPPER_LEFT:
                return "↖"
            case self.UPPER_RIGHT:
                return "↗"
            case self.LOWER_LEFT:
                return "↙"
            case self.LOWER_RIGHT:
                return "↘"
            case _:
                raise ValueError(f"Invalid direction: {self}")

    @property
    def clockwise(self) -> Direction:
        match self:
            case self.UP:
                return self.RIGHT
            case self.RIGHT:
                return self.DOWN
            case self.DOWN:
                return self.LEFT
            case self.LEFT:
                return self.UP
            case _:
                raise ValueError(
                    f"Invalid direction: {self} - maybe you meant clockwise8"
                )

    @property
    def clockwise8(self) -> Direction:
        match self:
            case self.UP:
                return self.UPPER_RIGHT
            case self.UPPER_RIGHT:
                return self.RIGHT
            case self.RIGHT:
                return self.LOWER_RIGHT
            case self.LOWER_RIGHT:
                return self.DOWN
            case self.DOWN:
                return self.LOWER_LEFT
            case self.LOWER_LEFT:
                return self.LEFT
            case self.LEFT:
                return self.UPPER_LEFT
            case self.UPPER_LEFT:
                return self.UP
            case _:
                raise ValueError(f"Invalid direction: {self}")

    @property
    def counter_clockwise(self) -> Direction:
        match self:
            case self.UP:
                return self.LEFT
            case self.LEFT:
                return self.DOWN
            case self.DOWN:
                return self.RIGHT
            case self.RIGHT:
                return self.UP
            case _:
                raise ValueError(
                    f"Invalid direction: {self} - maybe you meant counter_clockwise8"
                )

    @property
    def counter_clockwise8(self) -> Direction:
        match self:
            case self.UP:
                return self.UPPER_LEFT
            case self.UPPER_LEFT:
                return self.LEFT
            case self.LEFT:
                return self.LOWER_LEFT
            case self.LOWER_LEFT:
                return self.DOWN
            case self.DOWN:
                return self.LOWER_RIGHT
            case self.LOWER_RIGHT:
                return self.RIGHT
            case self.RIGHT:
                return self.UPPER_RIGHT
            case self.UPPER_RIGHT:
                return self.UP
            case _:
                raise ValueError(f"Invalid direction: {self}")

    @classmethod
    def from_str(cls, s: str) -> Direction:
        match s.upper():
            case "L" | "LEFT" | "WEST" | "W" | "<":
                return Direction.LEFT
            case "U" | "UP" | "NORTH" | "N" | "^":
                return Direction.UP
            case "R" | "RIGHT" | "EAST" | "E" | ">":
                return Direction.RIGHT
            case "D" | "DOWN" | "SOUTH" | "S" | "V":
                return Direction.DOWN
            case "UL" | "UPPER LEFT" | "NW" | "NORTHWEST":
                return Direction.UPPER_LEFT
            case "UR" | "UPPER RIGHT" | "NE" | "NORTHEAST":
                return Direction.UPPER_RIGHT
            case "LL" | "LOWER LEFT" | "SW" | "SOUTHWEST":
                return Direction.LOWER_LEFT
            case "LR" | "LOWER RIGHT" | "SE" | "SOUTHEAST":
                return Direction.LOWER_RIGHT
            case _:
                raise ValueError(f"Invalid direction: {s}")


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def translate(self, dx: int = 0, dy: int = 0) -> Point:
        return Point(self.x + dx, self.y + dy)

    def manhattan_distance(self, other: Point) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def euclidean_distance(self, other: Point) -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __iter__(self) -> Iterator[int]:
        return iter(astuple(self))

    def __lt__(self, other: Point) -> bool:
        return (self.y, self.x) < (other.y, other.x)

    def neighbor(self, direction: Direction) -> Point:
        match direction:
            case Direction.LEFT:
                return self.left
            case Direction.UP:
                return self.up
            case Direction.RIGHT:
                return self.right
            case Direction.DOWN:
                return self.down
            case Direction.UPPER_LEFT:
                return self.upper_left
            case Direction.UPPER_RIGHT:
                return self.upper_right
            case Direction.LOWER_LEFT:
                return self.bottom_left
            case Direction.LOWER_RIGHT:
                return self.bottom_right
            case _:
                raise ValueError(f"Invalid direction: {direction}")

    def neighbors_with_direction(
        self, *, include_diagonal: bool = False
    ) -> Iterator[tuple[Point, Direction]]:
        if include_diagonal:
            yield from (
                (self.left, Direction.LEFT),
                (self.right, Direction.RIGHT),
                (self.up, Direction.UP),
                (self.down, Direction.DOWN),
                (self.upper_left, Direction.UPPER_LEFT),
                (self.upper_right, Direction.UPPER_RIGHT),
                (self.bottom_left, Direction.LOWER_LEFT),
                (self.bottom_right, Direction.LOWER_RIGHT),
            )
        else:
            yield from (
                (self.left, Direction.LEFT),
                (self.right, Direction.RIGHT),
                (self.up, Direction.UP),
                (self.down, Direction.DOWN),
            )

    def neighbors(self, *, include_diagonal: bool = False) -> Iterator[Point]:
        yield from (
            p
            for p, _ in self.neighbors_with_direction(include_diagonal=include_diagonal)
        )

    @property
    def left(self) -> Point:
        return Point(self.x - 1, self.y)

    @property
    def right(self) -> Point:
        return Point(self.x + 1, self.y)

    @property
    def up(self) -> Point:
        return Point(self.x, self.y - 1)

    @property
    def down(self) -> Point:
        return Point(self.x, self.y + 1)

    @property
    def upper_left(self) -> Point:
        return Point(self.x - 1, self.y - 1)

    @property
    def upper_right(self) -> Point:
        return Point(self.x + 1, self.y - 1)

    @property
    def bottom_left(self) -> Point:
        return Point(self.x - 1, self.y + 1)

    @property
    def bottom_right(self) -> Point:
        return Point(self.x + 1, self.y + 1)

    @classmethod
    def num_inner_points(
        cls, positions: Iterable[Point], *, use_lines: bool = False
    ) -> int:
        shoelace = list(positions)
        shoelace.append(shoelace[0])
        area = 0
        if use_lines:
            num_points = 0
            for p1, p2 in zip(shoelace, shoelace[1:]):
                area += (p1.x * p2.y) - (p1.y * p2.x)
                num_points += p1.euclidean_distance(p2)
        else:
            num_points = len(shoelace) - 1
            for p1, p2 in zip(shoelace, shoelace[1:]):
                area += (p1.x * p2.y) - (p1.y * p2.x)
        return int(area / 2 - num_points / 2 + 1)
