#!/usr/bin/env python3
# www.jrodal.com

from math import sqrt
from rich.table import Table
from rich.console import Console
from typing import Callable, Generic, Iterable, Iterator, List, Tuple, Type, TypeVar


T = TypeVar("T")
U = TypeVar("U")


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

    def iter_coord_and_cell(self) -> Iterator[tuple[tuple[int, int], T]]:
        for i, cell in enumerate(self.data):
            x, y = i % self.w, i // self.w
            yield (x, y), cell

    def transform(self, func: Callable[[T], U]) -> "Grid[U]":
        transformed_data = [func(cell) for cell in self.data]
        return Grid[U](transformed_data, w=self.w, h=self.h)

    def transpose(self) -> "Grid[T]":
        return Grid([cell for col in self.cols() for cell in col], w=self.h, h=self.w)

    def rows(self) -> Iterator[Iterator[T]]:
        for r in range(self.h):
            yield (self.data[r * self.w + c] for c in range(self.w))

    def cols(self) -> Iterator[Iterator[T]]:
        for c in range(self.w):
            yield (self.data[r * self.w + c] for r in range(self.h))

    def at(self, x: int, y: int) -> T:
        return self.data[y * self.w + x]

    def left(self, x: int, y: int) -> T | None:
        return self.get(x - 1, y)

    def left_coord(self, x: int, y: int) -> tuple[int, int]:
        return x - 1, y

    def upper_left_coord(self, x: int, y: int) -> tuple[int, int]:
        return x - 1, y - 1

    def upper_right_coord(self, x: int, y: int) -> tuple[int, int]:
        return x + 1, y - 1

    def bottom_left_coord(self, x: int, y: int) -> tuple[int, int]:
        return x - 1, y + 1

    def bottom_right_coord(self, x: int, y: int) -> tuple[int, int]:
        return x + 1, y + 1

    def right_coord(self, x: int, y: int) -> tuple[int, int]:
        return x + 1, y

    def bottom_left(self, x: int, y: int) -> T | None:
        return self.get(x - 1, y + 1)

    def bottom_right(self, x: int, y: int) -> T | None:
        return self.get(x + 1, y + 1)

    def upper_left(self, x: int, y: int) -> T | None:
        return self.get(x - 1, y - 1)

    def upper_right(self, x: int, y: int) -> T | None:
        return self.get(x + 1, y - 1)

    def replace(self, x: int, y: int, value: T) -> None:
        self.data[y * self.w + x] = value

    def up_coord(self, x: int, y: int) -> tuple[int, int]:
        return x, y - 1

    def down_coord(self, x: int, y: int) -> tuple[int, int]:
        return x, y + 1

    def right(self, x: int, y: int) -> T | None:
        return self.get(x + 1, y)

    def up(self, x: int, y: int) -> T | None:
        return self.get(x, y - 1)

    def down(self, x: int, y: int) -> T | None:
        return self.get(x, y + 1)

    def find_cell(self, value: T) -> tuple[int, int]:
        i = self.data.index(value)
        return i % self.w, i // self.w

    def get(self, x: int, y: int, default: T | None = None) -> T | None:
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.at(x, y)
        else:
            return default

    def neighbors(
        self,
        x: int,
        y: int,
        *,
        include_diagonals: bool = False,
        include_self: bool = False
    ) -> Iterator[T]:
        for neighbor in self.neighbors_coordinates(
            x, y, include_diagonals=include_diagonals, include_self=include_self
        ):
            yield self.at(neighbor[0], neighbor[1])

    def neighbors_coordinates(
        self,
        x: int,
        y: int,
        *,
        include_diagonals: bool = False,
        include_self: bool = False
    ) -> Iterator[Tuple[int, int]]:
        if include_diagonals:
            dirs = self._DIRS_8
        else:
            dirs = self._DIRS

        if include_self:
            self_dx_xy = [(0, 0)]
        else:
            self_dx_xy = []

        for dx, dy in dirs + self_dx_xy:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.w and 0 <= ny < self.h:
                yield nx, ny

    @classmethod
    def taxicab_distance(cls, x1: int, y1: int, x2: int, y2: int) -> int:
        return abs(x1 - x2) + abs(y1 - y2)

    def display(self) -> None:
        table = Table(show_header=False, show_lines=True)
        for _ in range(self.w):
            table.add_column()
        for row in self.rows():
            table.add_row(*map(str, row))
        console = Console()
        console.print(table)
