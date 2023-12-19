#!/usr/bin/env python3
# www.jrodal.com

import re
from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        workflows_strs, ratings = self.data.split("\n\n")
        ratings = [[int(x) for x in re.findall(r"\d+", r)] for r in ratings.split()]

        # px{a<2006:qkq,m>2090:A,rfg}
        workflow_to_rule = {}
        for ws in workflows_strs.split():
            workflow_name, _, rule = ws.partition("{")  # }
            workflow_to_rule[workflow_name] = rule[:-1]

        total = 0
        for x, m, a, s in ratings:
            workflow = "in"
            while workflow not in ("A", "R"):
                for rule in workflow_to_rule[workflow].split(","):
                    if "<" in rule:
                        operator = "<"
                    elif ">" in rule:
                        operator = ">"
                    else:
                        workflow = rule
                        break
                    input, operator, comp_value_and_next_wf = rule.partition(operator)
                    comp_value, next_workflow = comp_value_and_next_wf.split(":")
                    comp_value = int(comp_value)

                    match input:
                        case "x":
                            value = x
                        case "m":
                            value = m
                        case "a":
                            value = a
                        case "s":
                            value = s
                        case _:
                            assert False

                    match operator:
                        case "<":
                            if value < comp_value:
                                workflow = next_workflow
                                break
                        case ">":
                            if value > comp_value:
                                workflow = next_workflow
                                break
                        case _:
                            assert False
            if workflow == "A":
                total += x + m + a + s
        return total

    def _part2(self) -> Solution:
        raise NotImplementedError
