#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.helpers import ints


class Computer:
    def __init__(self, program: list[int]):
        self.program = program

    def _get_combo_operand(self, operand: int, a: int, b: int, c: int) -> int:
        return [0, 1, 2, 3, a, b, c][operand]

    def run(
        self,
        a: int,
        b: int = 0,
        c: int = 0,
        pointer: int = 0,
    ) -> list[int]:
        out = []
        memory = [0, 1, 2, 3, a, b, c, 0, 0]
        a = 4
        b = 5
        c = 6
        pointer = 7
        operand = 8

        while memory[pointer] < len(self.program):
            opcode, memory[operand] = (
                self.program[memory[pointer]],
                self.program[memory[pointer] + 1],
            )

            match opcode:
                case 0 | 6 | 7:
                    memory[(opcode % 5) + 4] = memory[a] // (
                        2 ** memory[memory[operand]]
                    )
                case 1:
                    memory[b] ^= memory[operand]
                case 2:
                    memory[b] = memory[memory[operand]] % 8
                case 3:
                    if memory[a]:
                        memory[pointer] = memory[operand]
                        continue
                case 4:
                    memory[b] ^= memory[c]
                case 5:
                    out.append(memory[memory[operand]] % 8)
                case _:
                    assert False
            memory[pointer] += 2

        return out

    def create_spline(self) -> int:
        register_a = 0
        for offset in range(len(self.program)):
            desired_output = self.program[-(offset + 1) :]
            register_a = (register_a << 3) - 1
            while True:
                register_a += 1
                if self.run(register_a) == desired_output:
                    break

        return register_a


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        registers_str, program_str = self.sections()
        register_a = next(ints(registers_str)) if part1 else 0
        computer = Computer(list(ints(program_str)))
        if part1:
            return ",".join([str(i) for i in computer.run(register_a)])
        else:
            return computer.create_spline()
