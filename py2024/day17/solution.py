#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.helpers import ints
from math import gcd


class Solver(BaseSolver):
    def _get_combo_operand(
        self, operand: int, register_a: int, register_b: int, register_c: int
    ) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return register_a
            case 5:
                return register_b
            case 6:
                return register_c
            case _:
                assert False

    def _run_computer(
        self,
        register_a: int,
        register_b: int,
        register_c: int,
        program: list[int],
    ) -> list[int]:
        pointer = 0
        out = []
        while pointer < len(program):
            opcode = program[pointer]
            operand = program[pointer + 1]
            match opcode:
                case 0:
                    numerator = register_a
                    denominator = 2 ** (
                        self._get_combo_operand(
                            operand, register_a, register_b, register_c
                        )
                    )
                    register_a = numerator // denominator
                case 1:
                    register_b = register_b ^ operand
                case 2:
                    register_b = (
                        self._get_combo_operand(
                            operand, register_a, register_b, register_c
                        )
                        % 8
                    )
                case 3:
                    # 3, 5
                    if register_a:
                        pointer = operand
                        continue
                case 4:
                    register_b = register_b ^ register_c
                case 5:
                    out.append(
                        self._get_combo_operand(
                            operand, register_a, register_b, register_c
                        )
                        % 8
                    )
                case 6:
                    numerator = register_a
                    denominator = 2 ** (
                        self._get_combo_operand(
                            operand, register_a, register_b, register_c
                        )
                    )
                    register_b = numerator // denominator
                case 7:
                    numerator = register_a
                    denominator = 2 ** (
                        self._get_combo_operand(
                            operand, register_a, register_b, register_c
                        )
                    )
                    register_c = numerator // denominator
                case _:
                    assert False
            pointer += 2
        return out

    def _solve(self, part1: bool) -> Solution:
        registers_str, program_str = self.sections()
        register_a = next(ints(registers_str)) if part1 else 0
        register_b, register_c = 0, 0
        program = list(ints(program_str))
        if part1:
            return ",".join(
                [
                    str(i)
                    for i in self._run_computer(
                        register_a, register_b, register_c, program
                    )
                ]
            )

        for offset in range(len(program)):
            desired_output = program[-(offset + 1) :]
            register_a = (register_a << 3) - 1
            while True:
                register_a += 1
                result = self._run_computer(register_a, register_b, register_c, program)

                if result == desired_output:
                    break

        return register_a
