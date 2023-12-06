#!/usr/bin/env python3
# www.jrodal.com

import aocd
from rich.console import Console

# override this if you are solving for other years
YEAR = aocd.get.most_recent_year()
DAY = aocd.get.current_day()
CONSOLE = Console()
