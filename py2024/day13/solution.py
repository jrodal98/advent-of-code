#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
#
# from sympy import symbols, Eq, solve
#
# def find_min_tokens():
#     # Define variables
#     a, b = symbols('a b', integer=True)
#
#     # Define the equations
#     eq1 = Eq(94 * a + 22 * b, 8400)
#     eq2 = Eq(34 * a + 67 * b, 5400)
#
#     # Solve the equations
#     solution = solve((eq1, eq2), (a, b))
#
#     if solution:
#         # Extract the values of a and b
#         a = solution[a]
#         b = solution[b]
#
#         # Calculate the total cost
#         total_cost = 3 * a + b
#
#         return a, b, total_cost
#     else:
#         return None, None, None
#
# # Find and display the results
# a, b, total_cost = find_min_tokens()
# if a is not None:
#     print(f"Button A presses: {a}")
#     print(f"Button B presses: {b}")
#     print(f"Minimum tokens needed: {total_cost}")
# else:
#     print("No solution found.")


class Solver(BaseSolver):
    def _part1_helper(self, ax, ay, bx, by, x, y) -> int:
        min_tokens = float("inf")
        # Iterate through all possible values of a and b within the constraints
        for a_val in range(101):
            for b_val in range(101):
                if ax * a_val + bx * b_val == x and ay * a_val + by * b_val == y:
                    total_cost = 3 * a_val + b_val
                    if total_cost < min_tokens:
                        min_tokens = total_cost
        if min_tokens == float("inf"):
            return 0
        return min_tokens

    def _extract_ints(self, s: str) -> list[int]:
        ints = []
        for t in s.split():
            try:
                ints.append(int(t))
            except:
                pass
        return ints

    def _part1(self) -> Solution:
        ans = 0
        for line in self.data.split("\n\n"):
            lines = (
                line.replace(",", "").replace("+", " ").replace("=", " ").splitlines()
            )
            ax, ay = self._extract_ints(lines[0])
            bx, by = self._extract_ints(lines[1])
            x, y = self._extract_ints(lines[2])
            ans += self._part1_helper(ax, ay, bx, by, x, y)
        return ans

    def _part2(self) -> Solution:
        raise NotImplementedError
