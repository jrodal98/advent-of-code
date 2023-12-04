#!/usr/bin/env python3
# www.jrodal.com

from rich.table import Table
from rich.console import Console
from typing import Callable, Generic, Iterable, Iterator, List, Tuple, Type, TypeVar


T = TypeVar("T")
U = TypeVar("U")


class Grid(Generic[T]):
    _DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    _DIRS_8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def __init__(self, rows: List[List[T]]) -> None:
        self.rows = rows
        self.h = len(rows)
        self.w = len(rows[0]) if rows else 0

    @classmethod
    def from_lines(
        cls: Type["Grid[str]"], lines: str | Iterable[str], delimiter: str = ","
    ) -> "Grid[str]":
        if isinstance(lines, str):
            lines = lines.splitlines()

        rows = [[cell for cell in line.split(delimiter)] for line in lines]
        return cls(rows)

    def transform(self, func: Callable[[T], U]) -> "Grid[U]":
        transformed_rows = [[func(cell) for cell in row] for row in self.rows]
        return Grid[U](transformed_rows)

    def transpose(self) -> "Grid":
        transposed_rows = list(map(list, zip(*self.rows)))
        return Grid(transposed_rows)

    def at(self, x: int, y: int) -> T:
        return self.rows[y][x]

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

    def display(self) -> None:
        table = Table(show_header=False, show_lines=True)
        for _ in range(self.w):
            table.add_column()
        for row in self.rows:
            table.add_row(*map(str, row))
        console = Console()
        console.print(table)


if __name__ == "__main__":
    g = Grid.from_lines(["1,2,3", "4,5,6"]).transform(int)
    g.display()
    g2 = g.transform(lambda x: x**2)
    g2.display()
