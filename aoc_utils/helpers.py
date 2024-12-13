#!/usr/bin/env python3
# www.jrodal.com

import re
from typing import Iterator


def ints(s: str, *, include_sign=False) -> Iterator[int]:
    pattern = r"[-+]?\d+" if include_sign else r"\d+"
    return (int(m.group()) for m in re.finditer(pattern, s))
