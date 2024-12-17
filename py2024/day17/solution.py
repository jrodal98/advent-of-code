#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.helpers import ints


class Computer:
    def __init__(self, program: list[int]):
        self.program = program
        self.register_a = 0
        self.register_b = 0
        self.register_c = 0
        self.pointer = 0

    def reset(self, register_a: int) -> None:
        self.register_a = register_a
        self.register_b = 0
        self.register_c = 0
        self.pointer = 0

    def _get_combo_operand(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.register_a
            case 5:
                return self.register_b
            case 6:
                return self.register_c
            case _:
                assert False

    def run(self, register_a: int) -> list[int]:
        self.reset(register_a)
        out = []

        while self.pointer < len(self.program):
            opcode, operand = self.program[self.pointer], self.program[self.pointer + 1]

            match opcode:
                case 0:
                    self.register_a = self.register_a // (
                        2 ** self._get_combo_operand(operand)
                    )
                case 1:
                    self.register_b ^= operand
                case 2:
                    self.register_b = self._get_combo_operand(operand) % 8
                case 3:
                    if self.register_a:
                        self.pointer = operand
                        continue
                case 4:
                    self.register_b ^= self.register_c
                case 5:
                    out.append(self._get_combo_operand(operand) % 8)
                case 6:
                    self.register_b = self.register_a // (
                        2 ** self._get_combo_operand(operand)
                    )
                case 7:
                    self.register_c = self.register_a // (
                        2 ** self._get_combo_operand(operand)
                    )
                case _:
                    assert False
            self.pointer += 2

        return out

    def create_spline(self) -> int:
        register_a = 0
        for offset in range(len(self.program)):
            desired_output = self.program[-(offset + 1) :]
            register_a = (register_a << 3) - 1
            while True:
                register_a += 1
                if self.run(register_a=register_a) == desired_output:
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
