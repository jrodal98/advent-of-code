#!/usr/bin/env python3
# www.jrodal.com

from __future__ import annotations

from dataclasses import astuple, dataclass
from math import sqrt
from rich.table import Table
from rich.console import Console
from typing import Callable, Generic, Iterable, Iterator, List, Type, TypeVar


T = TypeVar("T")
U = TypeVar("U")


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

    def __init__(self, data: List[T], *, w: int | None, h: int | None) -> None:
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

    def iter(self) -> Iterator[tuple[Point, T]]:
        for i, cell in enumerate(self.data):
            x, y = i % self.w, i // self.w
            yield Point(x, y), cell

    def transform(self, func: Callable[[T], U]) -> "Grid[U]":
        transformed_data = [func(cell) for cell in self.data]
        return Grid[U](transformed_data, w=self.w, h=self.h)

    def transpose(self) -> "Grid[T]":
        return Grid(
            [cell for col in self.iter_cols() for cell in col], w=self.h, h=self.w
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

    def replace(self, p: Point, value: T) -> None:
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
        *,
        include_diagonals: bool = False,
        include_self: bool = False,
    ) -> Iterator[T]:
        for neighbor in self.neighbors_coordinates(
            p, include_diagonals=include_diagonals, include_self=include_self
        ):
            yield self.at(neighbor)

    def neighbors_coordinates(
        self,
        p: Point,
        *,
        include_diagonals: bool = False,
        include_self: bool = False,
    ) -> Iterator[Point]:
        if include_diagonals:
            dirs = self._DIRS_8
        else:
            dirs = self._DIRS

        if include_self:
            self_dx_xy = [(0, 0)]
        else:
            self_dx_xy = []

        for dx, dy in dirs + self_dx_xy:
            nx, ny = p.x + dx, p.y + dy
            if 0 <= nx < self.w and 0 <= ny < self.h:
                yield Point(nx, ny)

    def display(self) -> None:
        table = Table(show_header=False, show_lines=True)
        for _ in range(self.w):
            table.add_column()
        for row in self.iter_rows():
            table.add_row(*map(str, row))
        console = Console()
        console.print(table)
