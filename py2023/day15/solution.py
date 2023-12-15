#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.base_solver import BaseSolver, Solution


def compute_hash(s: str) -> int:
    current_value = 0
    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    assert current_value >= 0
    assert current_value <= 255
    return current_value


class Solver(BaseSolver):
    def _part1(self) -> Solution:
        sequence = self.data.strip().split(",")
        ans = 0
        for s in sequence:
            ans += compute_hash(s)
        return ans

    def _part2(self) -> Solution:
        sequence = self.data.strip().split(",")
        boxes: list[list[tuple[str, int]]] = []
        for i in range(256):
            boxes.append([])
        for s in sequence:
            if "=" in s:
                label, operator, focal_l = s.partition("=")
            else:
                label, operator, focal_l = s.partition("-")

            box_n = compute_hash(label)
            focal_l = int(focal_l or 0)
            box = boxes[box_n]

            if operator == "-":
                for i, (lbl, _) in enumerate(box):
                    if label == lbl:
                        box.pop(i)
                        break
            else:
                replaced = False
                for i, (lbl, _) in enumerate(box):
                    if label == lbl:
                        box[i] = (label, focal_l)
                        replaced = True
                        break
                if not replaced:
                    box.append((label, focal_l))

        ans = 0
        for box_n, box in enumerate(boxes):
            for slot_n, (_, focal_l) in enumerate(box):
                ans += (1 + box_n) * (1 + slot_n) * focal_l

        return ans
