#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from z3 import Int, Optimize, sat


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

    # def _part2_helper(self, ax, ay, bx, by, x, y) -> int:
    #     # Define z3 integer variables
    #     a_val = Int("a_val")
    #     b_val = Int("b_val")
    #
    #     # Create an optimizer instance
    #     opt = Optimize()
    #
    #     # Add constraints
    #     opt.add(ax * a_val + bx * b_val == x)
    #     opt.add(ay * a_val + by * b_val == y)
    #     opt.add(a_val >= 0, b_val >= 0)  # Assuming non-negative values for a and b
    #     opt.add(a_val >= 0, b_val >= 0)  # Assuming non-negative values for a and b
    #
    #     # Define the cost function and minimize it
    #     total_cost = 3 * a_val + b_val
    #     opt.minimize(total_cost)
    #
    #     # Check if the constraints are satisfiable
    #     if opt.check() == sat:
    #         model = opt.model()
    #         return model[total_cost].as_long()
    #     else:
    #         return 0  # Return 0 if no solution exists

    def _part2_helper(self, ax, ay, bx, by, x, y) -> int:
        # Define z3 integer variables
        a_val = Int("a_val")
        b_val = Int("b_val")

        # Create an optimizer instance
        opt = Optimize()

        # Add constraints
        opt.add(ax * a_val + bx * b_val == x)
        opt.add(ay * a_val + by * b_val == y)
        opt.add(a_val >= 0, b_val >= 0)  # Assuming non-negative values for a and b

        # Define the cost function and minimize it
        total_cost = 3 * a_val + b_val
        opt.minimize(total_cost)

        # Check if the constraints are satisfiable
        if opt.check() == sat:
            model = opt.model()
            # Extract values from the model to compute the total cost
            a_val_solution = model[a_val].as_long()
            b_val_solution = model[b_val].as_long()
            return 3 * a_val_solution + b_val_solution
        else:
            return 0  # Return 0 if no solution exists

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
        ans = 0
        for line in self.data.split("\n\n"):
            lines = (
                line.replace(",", "").replace("+", " ").replace("=", " ").splitlines()
            )
            ax, ay = self._extract_ints(lines[0])
            bx, by = self._extract_ints(lines[1])
            x, y = self._extract_ints(lines[2])
            ans += self._part2_helper(
                ax, ay, bx, by, x + 10000000000000, y + 10000000000000
            )
        if ans == 0:
            raise Exception("you are a dumbass")
        return ans
