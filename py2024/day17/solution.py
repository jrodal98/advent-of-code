#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from aoc_utils.helpers import ints


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
                    if register_a:
                        pointer = operand
                        continue
                case 4:
                    register_b = register_b ^ register_c
                case 5:
                    out.append(
                        str(
                            self._get_combo_operand(
                                operand, register_a, register_b, register_c
                            )
                            % 8
                        )
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
        return ",".join(out)

    def _try_a(
        self,
        register_a: int,
        register_b: int,
        register_c: int,
        program: list[int],
        seen: set[tuple[int, int, int, int]],
    ) -> list[int]:
        pointer = 0
        out = []
        while pointer < len(program):
            key = (register_a, register_b, register_c, pointer)
            # if key in seen:
            #     print(key)
            #     return False
            # seen.add(key)
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
                    res = (
                        self._get_combo_operand(
                            operand, register_a, register_b, register_c
                        )
                        % 8
                    )
                    # 2, 10, 18, 26
                    out.append(res)
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
        # a = 35184372088832
        # a = 35184375208445
        # a = 35184398801405
        # a = 35184793065981
        # a = 35186001025533
        a = 35204791507453
        shared = []
        while a < 1000000000000000000000000000000000000000000000000000000000000000:
            a += 8589934592
            out = self._try_a(a, register_b, register_c, program, set())

            if out == program:
                return a

            if out[:11] == program[:11]:
                print(a)
                shared.append(a)
                if len(shared) == 3:
                    for x, y in zip(shared, shared[1:]):
                        print(y - x)
                    assert False
        assert False
