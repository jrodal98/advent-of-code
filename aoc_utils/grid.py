#!/usr/bin/env python3
# www.jrodal.com

from __future__ import annotations
from copy import deepcopy

from dataclasses import astuple, dataclass
from enum import Enum
from math import sqrt
from rich.table import Table
from rich.console import Console
from typing import Callable, Generic, Iterable, Iterator, List, Type, TypeVar


T = TypeVar("T")
U = TypeVar("U")


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


class Grid(Generic[T]):
    _DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    _DIRS_8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def __init__(
        self, data: List[T], *, w: int | None = None, h: int | None = None
    ) -> None:
        len_data = len(data)
        if w is not None:
            self.w = w
            self.h = h or len_data // w
        elif h:
            self.w = len_data // h
            self.h = h
        else:
            rl = int(sqrt(len_data))
            self.w = rl
            self.h = rl

        assert self.w * self.h == len_data

        self.data = data

    @classmethod
    def from_lines(
        cls: Type["Grid[str]"],
        lines: str | Iterable[str],
        delimiter: str | None = None,
        padding: str | None = None,
    ) -> "Grid[str]":
        if isinstance(lines, str):
            lines = lines.splitlines()

        if delimiter:
            rows = [[cell for cell in line.split(delimiter)] for line in lines]
        else:
            rows = [[cell for cell in line] for line in lines]
        if padding:
            rows = [[padding, *row, padding] for row in rows]
            rows.insert(0, [padding] * len(rows[0]))
            rows.append([padding] * len(rows[0]))
        return cls([cell for row in rows for cell in row], w=len(rows[0]), h=len(rows))

    def iter(
        self,
        reverse: bool = False,
        disqualify: str | None = None,
        qualify: str | None = None,
    ) -> Iterator[tuple[Point, T]]:
        if reverse:
            for i in reversed(range(len(self.data))):
                x, y = i % self.w, i // self.w
                cell = self.data[i]
                if cell != disqualify and (not qualify or cell == qualify):
                    yield Point(x, y), cell
        else:
            for i, cell in enumerate(self.data):
                x, y = i % self.w, i // self.w
                if cell != disqualify and (not qualify or cell == qualify):
                    yield Point(x, y), cell

    def get_neighbor(
        self, p: Point | None, direction: Direction, default: T | None = None
    ) -> T | None:
        if not p:
            return None
        return self.get(p.neighbor(direction), default)

    def swap(self, p1: Point, p2: Point | Direction) -> Point:
        if isinstance(p2, Direction):
            p2 = p1.neighbor(p2)
        self.data[p1.y * self.w + p1.x], self.data[p2.y * self.w + p2.x] = (
            self.data[p2.y * self.w + p2.x],
            self.data[p1.y * self.w + p1.x],
        )
        return p2

    def transform(self, func: Callable[[T], U]) -> "Grid[U]":
        transformed_data = [func(cell) for cell in self.data]
        return Grid[U](transformed_data, w=self.w, h=self.h)

    def transpose(self) -> "Grid[T]":
        return Grid(
            [cell for col in self.iter_cols() for cell in col], w=self.h, h=self.w
        )

    def rotate(self) -> "Grid[T]":
        return Grid(
            [cell for col in self.iter_cols() for cell in reversed(list(col))],
            w=self.h,
            h=self.w,
        )

    def iter_rows(self) -> Iterator[Iterator[T]]:
        for r in range(self.h):
            yield (self.data[r * self.w + c] for c in range(self.w))

    def rows(self) -> list[list[T]]:
        return [list(r) for r in self.iter_rows()]

    def iter_cols(self) -> Iterator[Iterator[T]]:
        for c in range(self.w):
            yield (self.data[r * self.w + c] for r in range(self.h))

    def cols(self) -> list[list[T]]:
        return [list(c) for c in self.iter_cols()]

    def at(self, p: Point, *, allow_overflow: bool = False) -> T:
        x, y = p
        if allow_overflow:
            x, y = x % self.w, y % self.h
        return self.data[y * self.w + x]

    def replace(self, p: Point, value: T, color: str | None = None) -> None:
        if self.get(p) is None:
            return
        if color and isinstance(value, str):
            value = f"[{color}]{value}[/]"  # pyright: ignore
        self.data[p.y * self.w + p.x] = value

    def left(self, p: Point) -> T | None:
        return self.get(p.left)

    def right(self, p: Point) -> T | None:
        return self.get(p.right)

    def up(self, p: Point) -> T | None:
        return self.get(p.up)

    def down(self, p: Point) -> T | None:
        return self.get(p.down)

    def bottom_left(self, p: Point) -> T | None:
        return self.get(p.bottom_left)

    def bottom_right(self, p: Point) -> T | None:
        return self.get(p.bottom_right)

    def upper_left(self, p: Point) -> T | None:
        return self.get(p.upper_left)

    def upper_right(self, p: Point) -> T | None:
        return self.get(p.upper_right)

    def find(self, value: T) -> Point:
        i = self.data.index(value)
        return Point(i % self.w, i // self.w)

    def findall(self, value: T) -> Iterator[Point]:
        for p, c in self.iter():
            if c == value:
                yield p

    def get(
        self, p: Point, default: T | None = None, *, allow_overflow: bool = False
    ) -> T | None:
        if (0 <= p.x < self.w and 0 <= p.y < self.h) or allow_overflow:
            return self.at(p, allow_overflow=allow_overflow)
        else:
            return default

    def neighbors(
        self,
        p: Point,
        *,
        disqualify: str | None = None,
        qualify: str | None = None,
        allow_overflow: bool = False,
        include_diagonal: bool = False,
    ) -> Iterator[tuple[Point, T, Direction]]:
        for neighbor, direction in p.neighbors_with_direction(
            include_diagonal=include_diagonal
        ):
            v = self.get(neighbor, allow_overflow=allow_overflow)
            if v is not None and v != disqualify and (not qualify or v == qualify):
                yield neighbor, v, direction

    def display(self, rich: bool = False) -> None:
        if rich:
            table = Table(show_header=False, show_lines=True)
            for _ in range(self.w):
                table.add_column()
            for row in self.iter_rows():
                table.add_row(*map(str, row))
            console = Console()
            console.print(table)
        else:
            print(str(self))

    def __str__(self) -> str:
        return "\n".join("".join(map(str, r)) for r in self.iter_rows())

    def colored_str(
        self,
        points_to_colors: dict[Point | None, str] | None = None,
        values_to_color: dict[str | None, str] | None = None,
    ) -> str:
        points_to_colors = points_to_colors or {}
        values_to_color = values_to_color or {}

        res = ["" for _ in range(self.h)]
        for i, cell in enumerate(self.data):
            x, y = i % self.w, i // self.w
            color = points_to_colors.get(Point(x, y), values_to_color.get(str(cell)))
            if color:
                # this is to prevent \[{color}] from being escaped
                if res[y]:
                    if (len(res[y]) == 1 and res[y][-1] == "\\") or (
                        len(res[y]) >= 2 and res[y][-1] == "\\" and res[y][-2] != "\\"
                    ):
                        res[y] += "\\"
                if cell == "\\":
                    cell = "\\\\"
                res[y] += f"[{color}]{cell}[/{color}]"
            else:
                res[y] += str(cell)
        return "\n".join(res)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Grid):
            return False
        return self.data == other.data

    def __hash__(self) -> int:
        return hash(tuple(self.data)) + hash(self.w) - hash(self.h)

    def copy(self) -> "Grid[T]":
        return deepcopy(self)


if __name__ == "__main__":
    grid = Grid.from_lines("123\n456\n789")
    grid.display()
    grid.display(True)
