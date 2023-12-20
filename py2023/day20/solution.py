#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution
from collections import deque


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        flip_flops = {}
        conjunctions = {}
        broadcaster = []
        module_states = {}
        # %fg -> nt, gt
        # &nt -> rq, fg, ft, nd, gt, xz
        # broadcaster -> pj, fg, bh, br
        for line in self.data.splitlines():
            from_module, to_module = line.split(" -> ")
            modules = to_module.split(", ")
            if from_module == "broadcaster":
                broadcaster = modules
                module_states["broadcaster"] = False
            elif from_module[0] == "%":
                flip_flops[from_module[1:]] = modules
                module_states[from_module[1:]] = False
            else:
                conjunctions[from_module[1:]] = modules
                module_states[from_module[1:]] = {}

        for k, modules in flip_flops.items():
            for m in modules:
                if m in conjunctions:
                    module_states[m][k] = False
        for k, modules in conjunctions.items():
            for m in modules:
                if m in conjunctions:
                    module_states[m][k] = False
        # for m in broadcaster:
        #     if m in conjunctions:
        #         module_states[m]["broadcaster"] = True

        signals_to_process: deque[tuple[str, str, bool]] = deque(
            [("broadcaster", "button", False)]
        )
        low_pulses = 0
        high_pulses = 0
        button_presses = 0
        while button_presses < 1000 or signals_to_process:
            if signals_to_process:
                (
                    current_module,
                    input_module,
                    input_signal,
                ) = signals_to_process.popleft()
            else:
                current_module, input_module, input_signal = (
                    "broadcaster",
                    "button",
                    False,
                )
            # print(
            #     f"{input_module} -{'high' if input_signal else 'low'}-> {current_module}"
            # )
            # print(module_states)

            if current_module in flip_flops:
                if input_signal:
                    continue

                output_signal = not module_states[current_module]
                module_states[current_module] = output_signal
                for next_module in flip_flops[current_module]:
                    signals_to_process.append(
                        (next_module, current_module, output_signal)
                    )
                    if output_signal:
                        high_pulses += 1
                    else:
                        low_pulses += 1

            elif current_module in conjunctions:
                if input_module in module_states[current_module]:
                    module_states[current_module][input_module] = input_signal
                output_signal = not all(module_states[current_module].values())
                # Then, if it remembers high pulses for all inputs, it sends a low pulse;
                # otherwise, it sends a high pulse.

                for next_module in conjunctions[current_module]:
                    signals_to_process.append(
                        (next_module, current_module, output_signal)
                    )
                    if output_signal:
                        high_pulses += 1
                    else:
                        low_pulses += 1

            else:
                button_presses += 1
                low_pulses += 1
                for next_module in broadcaster:
                    signals_to_process.append((next_module, current_module, False))
                    low_pulses += 1
        print(button_presses, low_pulses, high_pulses)
        return low_pulses * high_pulses

    def _part2(self) -> Solution:
        raise NotImplementedError
