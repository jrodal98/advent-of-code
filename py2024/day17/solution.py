#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.helpers import ints


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        registers_str, program_str = self.sections()
        a = next(ints(registers_str)) if part1 else 0
        computer = Computer(list(ints(program_str)))
        if part1:
            return ",".join(map(str, computer.run(a)))
        else:
            return computer.create_spline()


class Computer:
    def __init__(self, program: list[int]):
        self.program = program
        # storing pointers not because it's practical, but because it's fun
        self.a = 4
        self.b = 5
        self.c = 6
        self.pointer = 7
        self.operand = 8

    def run(
        self,
        a_val: int,
    ) -> list[int]:
        out = []
        # storing memory not because it's practical, but because it's fun
        memory = [0, 1, 2, 3, a_val, 0, 0, 0, 0]

        while memory[self.pointer] < len(self.program):
            opcode, memory[self.operand] = (
                self.program[memory[self.pointer]],
                self.program[memory[self.pointer] + 1],
            )

            match opcode:
                case 0 | 6 | 7:
                    memory[(opcode % 5) + 4] = memory[self.a] // (
                        2 ** memory[memory[self.operand]]
                    )
                case 2 | 5:
                    res = memory[memory[self.operand]] % 8
                    if opcode == 5:
                        out.append(res)
                    else:
                        memory[self.b] = res
                case 3:
                    if memory[self.a]:
                        memory[self.pointer] = memory[self.operand]
                        continue
                case _:
                    memory[self.b] ^= memory[self.operand if opcode == 1 else self.c]
            memory[self.pointer] += 2

        return out

    def create_spline(self) -> int:
        a = 0
        for offset in range(len(self.program)):
            desired_output = self.program[-(offset + 1) :]
            a = (a << 3) - 1
            while True:
                a += 1
                if self.run(a) == desired_output:
                    break

        return a
