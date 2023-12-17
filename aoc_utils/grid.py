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


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def translate(self, dx: int = 0, dy: int = 0) -> Point:
        return Point(self.x + dx, self.y + dy)

    def manhattan_distance(self, other: Point) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def euiclean_distance(self, other: Point) -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __iter__(self) -> Iterator[int]:
        return iter(astuple(self))

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

    def neighbors_with_direction(self) -> Iterator[tuple[Point, Direction]]:
        yield from (
            (self.left, Direction.LEFT),
            (self.right, Direction.RIGHT),
            (self.up, Direction.UP),
            (self.down, Direction.DOWN),
        )

    def neighbors(self) -> Iterator[Point]:
        yield from (p for p, _ in self.neighbors_with_direction())

    def neighbors8_with_direction(self) -> Iterator[tuple[Point, Direction]]:
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

    def neighbors8(self) -> Iterator[Point]:
        yield from (p for p, _ in self.neighbors8_with_direction())

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

    def iter(self, reverse: bool = False) -> Iterator[tuple[Point, T]]:
        if reverse:
            for i in reversed(range(len(self.data))):
                x, y = i % self.w, i // self.w
                yield Point(x, y), self.data[i]
        else:
            for i, cell in enumerate(self.data):
                x, y = i % self.w, i // self.w
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

    def at(self, p: Point) -> T:
        return self.data[p.y * self.w + p.x]

    def replace(self, p: Point, value: T, color: str | None = None) -> None:
        if not self.get(p):
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

    def find_cell(self, value: T) -> Point:
        i = self.data.index(value)
        return Point(i % self.w, i // self.w)

    def get(self, p: Point, default: T | None = None) -> T | None:
        if 0 <= p.x < self.w and 0 <= p.y < self.h:
            return self.at(p)
        else:
            return default

    def neighbors(
        self,
        p: Point,
    ) -> Iterator[T]:
        for neighbor in p.neighbors():
            v = self.get(neighbor)
            if v:
                yield v

    def neighbors_with_direction(self, p: Point) -> Iterator[tuple[T, Direction]]:
        for neighbor, direction in p.neighbors_with_direction():
            v = self.get(neighbor)
            if v:
                yield v, direction

    def neighbors8(self, p: Point) -> Iterator[T]:
        for neighbor in p.neighbors8():
            v = self.get(neighbor)
            if v:
                yield v

    def neighbors8_with_direction(self, p: Point) -> Iterator[tuple[T, Direction]]:
        for neighbor, direction in p.neighbors8_with_direction():
            v = self.get(neighbor)
            if v:
                yield v, direction

    def display(self, rich: bool = True) -> None:
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

    def colored_str(self, points_to_colors: dict[Point | None, str]) -> str:
        res = ["" for _ in range(self.h)]
        for i, cell in enumerate(self.data):
            x, y = i % self.w, i // self.w
            color = points_to_colors.get(Point(x, y))
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
    grid.display(False)
