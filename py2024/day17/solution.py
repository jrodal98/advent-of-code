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

    def _part1(self) -> Solution:
        registers_str, program_str = self.sections()
        register_a, register_b, register_c = ints(registers_str.replace("\n", ""))
        program = list(ints(program_str))
        out = self._run_computer(register_a, register_b, register_c, program)
        return ",".join([str(i) for i in out])

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

    def _part2(self) -> Solution:
        registers_str, program_str = self.sections()
        _, register_b, register_c = ints(registers_str.replace("\n", ""))
        program = list(ints(program_str))
        rprog = program.copy()
        rprog.reverse()
        N = len(program)
        register_a = 0
        for i in range(N):
            want = program[N - i - 1 :]
            t = 0
            while True:
                aprime = (register_a << 3) + t
                result = self._run_computer(aprime, register_b, register_c, program)
                if result == want:
                    register_a = aprime
                    break
                t += 1
        return register_a
