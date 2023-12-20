#!/usr/bin/env python3
# www.jrodal.com

from copy import deepcopy
from aoc_utils.base_solver import BaseSolver, Solution
from collections import deque

from math import lcm


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        flip_flops = {}
        conjunctions = {}
        broadcaster = []
        module_states = {}
        for line in self.data.splitlines():
            from_module, to_module = line.split(" -> ")
            modules = to_module.split(", ")
            if from_module == "broadcaster":
                broadcaster = modules
                module_states["broadcaster"] = False
            elif from_module[0] == "%":
                flip_flops[from_module[1:]] = modules
                module_states[from_module[1:]] = False
            elif from_module[0] == "&":
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

            elif current_module == "broadcaster":
                button_presses += 1
                low_pulses += 1
                for next_module in broadcaster:
                    signals_to_process.append((next_module, current_module, False))
                    low_pulses += 1
        return low_pulses * high_pulses

    def _part2(self) -> Solution:
        flip_flops = {}
        conjunctions = {}
        broadcaster = []
        module_states = {}
        for line in self.data.splitlines():
            from_module, to_module = line.split(" -> ")
            modules = to_module.split(", ")
            if from_module == "broadcaster":
                broadcaster = modules
                module_states["broadcaster"] = False
            elif from_module[0] == "%":
                flip_flops[from_module[1:]] = modules
                module_states[from_module[1:]] = False
            elif from_module[0] == "&":
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

        signals_to_process: deque[tuple[str, str, bool]] = deque(
            [("broadcaster", "button", False)]
        )
        low_pulses = 0
        high_pulses = 0

        flip_flops_bak = flip_flops.copy()
        conjunctions_bak = conjunctions.copy()
        broadcaster_bak = broadcaster.copy()
        module_states_bak = module_states.copy()

        # this will only work for my puzzle input
        critical_nodes = ["sb", "nd", "ds", "hf"]
        cycle_lengths = []
        for node in critical_nodes:
            signals_to_process: deque[tuple[str, str, bool]] = deque(
                [("broadcaster", "button", False)]
            )
            flip_flops = deepcopy(flip_flops_bak)
            conjunctions = deepcopy(conjunctions_bak)
            broadcaster = deepcopy(broadcaster_bak)
            module_states = deepcopy(module_states_bak)
            button_presses = 0
            last_omitted_signal = False
            while not last_omitted_signal or signals_to_process:
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

                    if current_module == node and output_signal:
                        last_omitted_signal = True

                    for next_module in conjunctions[current_module]:
                        signals_to_process.append(
                            (next_module, current_module, output_signal)
                        )
                        if output_signal:
                            high_pulses += 1
                        else:
                            low_pulses += 1

                elif current_module == "broadcaster":
                    button_presses += 1
                    low_pulses += 1
                    for next_module in broadcaster:
                        signals_to_process.append((next_module, current_module, False))
                        low_pulses += 1
            cycle_lengths.append(button_presses)
        return lcm(*cycle_lengths)
