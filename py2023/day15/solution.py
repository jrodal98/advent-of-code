#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    def _compute_hash(self, s: str) -> int:
        current_value = 0
        for c in s:
            current_value += ord(c)
            current_value *= 17
            current_value %= 256
        return current_value

    def _part1(self) -> Solution:
        sequence = self.data.strip().split(",")
        return sum(self._compute_hash(s) for s in sequence)

    def _part2(self) -> Solution:
        sequence = self.data.strip().split(",")
        boxes: list[list[str]] = [[] for _ in range(256)]
        focal_lengths = {}
        for s in sequence:
            label, operator, focal_l = s.partition(s[max(s.find("="), s.find("-"))])
            box = boxes[self._compute_hash(label)]
            label_in_box = label in box
            focal_lengths[label] = int(focal_l or 0)
            match operator, label_in_box:
                case "-", True:
                    box.remove(label)
                case "=", False:
                    box.append(label)
        return sum(
            box_n * slot_n * focal_lengths[lbl]
            for box_n, box in enumerate(boxes, 1)
            for slot_n, lbl in enumerate(box, 1)
        )
