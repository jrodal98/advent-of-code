#!/usr/bin/env python3
# www.jrodal.com


def part1(s: str) -> int:
    res = 0
    for game_id, line in enumerate(s.splitlines(), 1):
        bad = False
        _, sets = line.split(": ")
        sets = sets.split("; ")
        for st in sets:
            if bad:
                break
            color_strings = st.split(", ")
            for cs in color_strings:
                n, col = cs.split()
                n = int(n)
                if (
                    (col == "red" and n > 12)
                    or (col == "green" and n > 13)
                    or (col == "blue" and n > 14)
                ):
                    bad = True
                    break
        if not bad:
            res += game_id

    return res


def part2(s: str) -> int:
    res = 0
    for line in s.splitlines():
        max_color_counts = {"red": 0, "blue": 0, "green": 0}
        _, sets = line.split(": ")
        sets = sets.split("; ")
        for st in sets:
            color_strings = st.split(", ")
            for cs in color_strings:
                n, col = cs.split()
                n = int(n)
                max_color_counts[col] = max(n, max_color_counts[col])
        res += (
            max_color_counts["red"]
            * max_color_counts["blue"]
            * max_color_counts["green"]
        )

    return res


if __name__ == "__main__":
    import sys

    with open(sys.argv[1]) as f:
        s = f.read().strip()

    print(f"Part 1: {part1(s)}")
    print(f"Part 2: {part2(s)}")
