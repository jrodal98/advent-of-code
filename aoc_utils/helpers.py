#!/usr/bin/env python3
# www.jrodal.com

import re


def ints(s: str, *, include_sign=False) -> list[int]:
    pattern = r"[-+]?\d+" if include_sign else r"\d+"
    return [int(i) for i in re.findall(pattern, s)]
