#!/usr/bin/env python3
# www.jrodal.com

from __future__ import annotations
from copy import deepcopy

from math import sqrt
from rich.table import Table
from rich.console import Console
from typing import Callable, Generic, Iterable, Iterator, List, Type, TypeVar

from aoc_utils.point import Direction, Point


T = TypeVar("T")
U = TypeVar("U")


class Grid(Generic[T]):
    def __init__(
        self,
        data: List[T],
        *,
        w: int | None = None,
        h: int | None = None,
        allow_overflow: bool = False,
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
        self.allow_overflow = allow_overflow

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

    def fill(self, value: T) -> None:
        self.data = [value] * self.w * self.h

    def _should_include(
        self,
        point: Point,
        cell: T,
        exclude: T | Callable[[Point, T], bool] | None = None,
        include: T | Callable[[Point, T], bool] | None = None,
    ) -> bool:
        if exclude is not None:
            if callable(exclude):
                if exclude(point, cell):
                    return False
            elif cell == exclude:
                return False

        if include is not None:
            if callable(include):
                if not include(point, cell):
                    return False
            elif cell != include:
                return False

        return True

    def iter(
        self,
        reverse: bool = False,
        exclude: T | Callable[[Point, T], bool] | None = None,
        include: T | Callable[[Point, T], bool] | None = None,
    ) -> Iterator[tuple[Point, T]]:
        if reverse:
            for i in reversed(range(len(self.data))):
                x, y = i % self.w, i // self.w
                cell = self.data[i]
                point = Point(x, y)
                if self._should_include(point, cell, exclude, include):
                    yield point, cell
        else:
            for i, cell in enumerate(self.data):
                x, y = i % self.w, i // self.w
                point = Point(x, y)
                if self._should_include(point, cell, exclude, include):
                    yield point, cell

    def __iter__(self) -> Iterator[tuple[Point, T]]:
        # Call iter without filters or reverse
        return self.iter()

    def get_neighbor(
        self, p: Point | None, direction: Direction, default: T | None = None
    ) -> T | None:
        if not p:
            return None
        return self.get(p.neighbor(direction), default)

    def walk_directions(
        self,
        p,
        directions: Iterable[Direction],
        default: T | None = None,
        include_start: bool = False,
    ) -> Iterator[T | None]:
        if include_start:
            yield self.get(p, default)
        for direction in directions:
            p = p.neighbor(direction)
            yield self.get(p, default)

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

    def __getitem__(self, p: Point) -> T:
        return self.at(p)

    def __setitem__(self, p: Point, value: T) -> None:
        self.replace(p, value)

    def _allow_overflow(self, allow_overflow: bool | None) -> bool:
        if allow_overflow is None:
            return self.allow_overflow
        return allow_overflow

    def at(self, p: Point, *, allow_overflow: bool | None = None) -> T:
        x, y = p.x, p.y
        if self._allow_overflow(allow_overflow):
            x, y = x % self.w, y % self.h
        return self.data[y * self.w + x]

    def replace(
        self,
        p: Point,
        value: T,
        color: str | None = None,
        allow_overflow: bool | None = None,
    ) -> None:
        x, y = p.x, p.y
        if self._allow_overflow(allow_overflow):
            x, y = x % self.w, y % self.h
        elif self.get(p) is None:
            return
        if color and isinstance(value, str):
            value = f"[{color}]{value}[/{color}]"  # pyright: ignore
        self.data[y * self.w + x] = value

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
        self, p: Point, default: T | None = None, *, allow_overflow: bool | None = None
    ) -> T | None:
        if (0 <= p.x < self.w and 0 <= p.y < self.h) or (
            allow_overflow := self._allow_overflow(allow_overflow)
        ):
            return self.at(p, allow_overflow=allow_overflow)
        else:
            return default

    def inbounds(self, p: Point) -> bool:
        return 0 <= p.x < self.w and 0 <= p.y < self.h

    def neighbors(
        self,
        p: Point,
        *,
        exclude: T | Callable[[Point, T], bool] | None = None,
        include: T | Callable[[Point, T], bool] | None = None,
        allow_overflow: bool = False,
        include_diagonal: bool = False,
    ) -> Iterator[tuple[Point, T, Direction]]:
        for neighbor, direction in p.neighbors_with_direction(
            include_diagonal=include_diagonal
        ):
            v = self.get(neighbor, allow_overflow=allow_overflow)
            if v is not None and self._should_include(neighbor, v, exclude, include):
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
