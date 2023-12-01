#!/usr/bin/env python3
# www.jrodal.com

import re


def part1(s: str) -> int:
    res = 0
    for line in s.split():
        digits = []
        for c in line:
            try:
                int(c)
                digits.append(c)
            except Exception:
                pass
        res += int(digits[0] + digits[-1])
    return res


def part2(s: str) -> int:
    rep = {
        "one": "1e",
        "two": "2o",
        "three": "3e",
        "four": "4r",
        "five": "5e",
        "six": "6x",
        "seven": "7n",
        "eight": "8t",
        "nine": "9e",
    }

    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    s = pattern.sub(lambda m: rep[re.escape(m.group(0))], s)
    s = pattern.sub(lambda m: rep[re.escape(m.group(0))], s)
    return part1(s)


if __name__ == "__main__":
    import sys

    with open(sys.argv[1]) as f:
        s = f.read().strip()

    # print(f"Part 1: {part1(s)}")
    print(f"Part 2: {part2(s)}")
