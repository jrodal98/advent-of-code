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
        workflows_strs, ratings = self.data.split("\n\n")
        ratings = [[int(x) for x in re.findall(r"\d+", r)] for r in ratings.split()]

        # px{a<2006:qkq,m>2090:A,rfg}
        workflow_to_rule = {}
        for ws in workflows_strs.split():
            workflow_name, _, rule = ws.partition("{")  # }
            workflow_to_rule[workflow_name] = rule[:-1]

        total = 0
        states_to_check: list[
            tuple[
                tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], str
            ]
        ] = [((1, 4000), (1, 4000), (1, 4000), (1, 4000), "in")]
        while states_to_check:
            x, m, a, s, workflow = states_to_check.pop()
            if workflow == "R":
                continue
            elif workflow == "A":
                total += (
                    (x[1] - x[0] + 1)
                    * (m[1] - m[0] + 1)
                    * (a[1] - a[0] + 1)
                    * (s[1] - s[0] + 1)
                )
                continue

            for rule in workflow_to_rule[workflow].split(","):
                if "<" in rule:
                    operator = "<"
                elif ">" in rule:
                    operator = ">"
                else:
                    states_to_check.append((x, m, a, s, rule))
                    break

                letter, operator, comp_value_and_next_wf = rule.partition(operator)
                comp_value, next_workflow = comp_value_and_next_wf.split(":")
                comp_value = int(comp_value)

                match letter, operator:
                    case "x", ">":
                        min_x, max_x = x
                        # condition is met, check next workflow
                        if min_x > comp_value:
                            states_to_check.append((x, m, a, s, next_workflow))
                            break
                        # condition is not met in any scenario, check next rule
                        elif max_x <= comp_value:
                            continue
                        else:
                            # x no longer meets condition
                            states_to_check.append(
                                ((min_x, comp_value), m, a, s, workflow)
                            )
                            # x always meets condition
                            states_to_check.append(
                                ((comp_value + 1, max_x), m, a, s, workflow)
                            )
                            break
                    case "x", "<":
                        min_x, max_x = x
                        # condition is met, check next workflow
                        if max_x < comp_value:
                            states_to_check.append((x, m, a, s, next_workflow))
                            break
                        # condition is not met in any scenario, check next rule
                        elif min_x >= comp_value:
                            continue
                        else:
                            # x always meets the condition
                            states_to_check.append(
                                ((min_x, comp_value - 1), m, a, s, workflow)
                            )
                            # x never meets the condition
                            states_to_check.append(
                                ((comp_value, max_x), m, a, s, workflow)
                            )
                            break
                    case "m", ">":
                        min_m, max_m = m
                        if min_m > comp_value:
                            states_to_check.append((x, m, a, s, next_workflow))
                            break
                        elif max_m <= comp_value:
                            continue
                        else:
                            states_to_check.append(
                                (x, (min_m, comp_value), a, s, workflow)
                            )
                            states_to_check.append(
                                (x, (comp_value + 1, max_m), a, s, workflow)
                            )
                            break
                    case "m", "<":
                        min_m, max_m = m
                        if max_m < comp_value:
                            states_to_check.append((x, m, a, s, next_workflow))
                            break
                        elif min_m >= comp_value:
                            continue
                        else:
                            states_to_check.append(
                                (x, (min_m, comp_value - 1), a, s, workflow)
                            )
                            states_to_check.append(
                                (x, (comp_value, max_m), a, s, workflow)
                            )
                            break
                    case "a", ">":
                        min_a, max_a = a
                        if min_a > comp_value:
                            states_to_check.append((x, m, a, s, next_workflow))
                            break
                        elif max_a <= comp_value:
                            continue
                        else:
                            states_to_check.append(
                                (x, m, (min_a, comp_value), s, workflow)
                            )
                            states_to_check.append(
                                (x, m, (comp_value + 1, max_a), s, workflow)
                            )
                            break
                    case "a", "<":
                        min_a, max_a = a
                        if max_a < comp_value:
                            states_to_check.append((x, m, a, s, next_workflow))
                            break
                        elif min_a >= comp_value:
                            continue
                        else:
                            states_to_check.append(
                                (x, m, (min_a, comp_value - 1), s, workflow)
                            )
                            states_to_check.append(
                                (x, m, (comp_value, max_a), s, workflow)
                            )
                            break
                    case "s", ">":
                        min_s, max_s = s
                        if min_s > comp_value:
                            states_to_check.append((x, m, a, s, next_workflow))
                            break
                        elif max_s <= comp_value:
                            continue
                        else:
                            states_to_check.append(
                                (x, m, a, (min_s, comp_value), workflow)
                            )
                            states_to_check.append(
                                (x, m, a, (comp_value + 1, max_s), workflow)
                            )
                            break
                    case "s", "<":
                        min_s, max_s = s
                        if max_s < comp_value:
                            states_to_check.append((x, m, a, s, next_workflow))
                            break
                        elif min_s >= comp_value:
                            continue
                        else:
                            states_to_check.append(
                                (x, m, a, (min_s, comp_value - 1), workflow)
                            )
                            states_to_check.append(
                                (x, m, a, (comp_value, max_s), workflow)
                            )
                            break
                    case _, _:
                        assert False

        return total
