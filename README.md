# Advent of code

https://adventofcode.com/2024

# How to use repository

1. Download `direnv`
2. Store AOC session cookie in `.env` file (e.g. `export AOC_SESSION=...`)
3. `pip install -r requirements.txt`
4. `init` to setup template
5. `solve` to test and submit solutions
6. Use `init --help` and `solve --help` for more advanced usage
7. If `init` and `solve` aren't working, try `python main.py init`, etc

# Available Scripts

The repository includes several convenience scripts in the `scripts/` directory:

## init

Initialize a new day's solution from template.

```bash
# Initialize today's problem
init

# Initialize specific day/year
init --day 5 --year 2024
python main.py init --day 5 --year 2024

# Get help
init --help
```

**What it does:**
- Creates a new directory (e.g., `py2024/day05/`)
- Copies template files (`solution.py`, `tests.py`, `manifest.yaml`)
- Sets up the basic structure for solving the problem

## solve

Run tests and solve the problem with automatic submission to Advent of Code.

```bash
# Solve today's problem (runs tests, then solves both parts)
solve

# Solve specific day/year
solve --day 5 --year 2024

# Skip tests and just solve
solve --skip-tests

# Only solve part 1
solve --skip-part2

# Only solve part 2
solve --skip-part1

# Use custom input instead of downloading
solve --input sample1.txt
solve --input "custom input data"

# Get help with all options
solve --help
```

**Advanced options:**

```bash
# Animate the solution (if _update_animation is used)
solve --animate

# Add lag to animation (in milliseconds)
solve --animate --lag 100

# Step through animation manually (press Enter for each step)
solve --animate --step
```

**What it does:**
1. Runs unit tests from `manifest.yaml`
2. Downloads puzzle input from Advent of Code (or uses `--input`)
3. Runs your `_part1()` and `_part2()` methods
4. Displays performance metrics
5. Automatically submits answers to Advent of Code
6. Shows Rich-formatted output with syntax highlighting

## debug

Same as `solve` but with enhanced error reporting.

```bash
# Solve with local variable logging in tracebacks
debug

# All solve options work
debug --day 5 --skip-tests
```

**What it does:**
- Runs `solve --log-locals` to show local variable values in error tracebacks
- Helpful for debugging when your solution crashes

## edit

Quick editor launcher for modified/new files.

```bash
# Opens recently modified solution files in your editor
edit
```

**What it does:**
- Finds recently modified or new files: `solution.py`, `sample1.txt`, `test_manifest.yml`
- Opens them all in your `$EDITOR`
- Useful workflow: `init`, `edit`, make changes, `solve`

# Workflow Examples

## Starting a new day

```bash
# Initialize day's template
init

# Open files for editing
edit

# Write solution in solution.py, add test cases to manifest.yaml

# Test and solve
solve

# If errors occur, debug with locals
debug
```

## Working on a specific day

```bash
# Solve day 12 of 2023
solve --day 12 --year 2023

# Test with sample input first
solve --day 12 --input sample1.txt

# Then solve with real input
solve --day 12
```

## Animation workflow

```bash
# Add animation to your solution
self._set_animation_grid()
self._update_animation(point=pos, value="X")

# View animation
solve --animate --lag 50

# Step through slowly
solve --animate --step
```

# aoc_utils Library Guide

The `aoc_utils` library provides powerful utilities for solving Advent of Code problems efficiently.

## BaseSolver

Core class that all solutions inherit from. Provides automatic input parsing, solution submission, and performance tracking.

### Basic Structure

```python
from aoc_utils.base_solver import BaseSolver, Solution

class Solver(BaseSolver):
    def _part1(self) -> Solution:
        # Your solution here
        return answer

    def _part2(self) -> Solution:
        # Your solution here
        return answer
```

### Input Parsing Methods

```python
# Parse lines
self.lines()  # Returns list[str] of all lines

# Parse sections (separated by blank lines)
self.sections()  # Returns list[str] of sections

# Access raw data
self.data  # The raw input string (with trailing newlines stripped)

# Parse as grid (automatically creates Grid[str])
self.grid  # Returns Grid[str] from input
```

**Example from Day 1:**
```python
def _get_lists(self) -> tuple[list[int], list[int]]:
    left = []
    right = []
    for line in self.lines():
        lv, rv = line.split()
        left.append(int(lv))
        right.append(int(rv))
    return left, right
```

### Animation Support

Visualize your algorithm with built-in animation support:

```python
def _part1(self) -> Solution:
    self._set_animation_grid()  # Enable animation

    # Update during algorithm
    self._update_animation(
        point=current_pos,
        value="X",  # Or a function: lambda grid, p: some_value
        message="Step 42",
        points_to_colors={current_pos: "green", target: "red"},
        values_to_colors={"#": "blue", ".": "white"}
    )
```

**Example from Day 6:**
```python
self._update_animation(
    point=new_pos,
    value=dir.arrow,  # Shows direction arrow
)
```

## Grid

Powerful 2D grid with pathfinding, neighbor iteration, and transformation utilities.

### Creating Grids

```python
from aoc_utils.grid import Grid
from aoc_utils.point import Point

# From input (most common)
grid = Grid.from_lines(self.data)

# With delimiter
grid = Grid.from_lines(data, delimiter=",")

# With padding
grid = Grid.from_lines(data, padding=".")

# From scratch
grid = Grid(data=["."] * 100, w=10, h=10)

# With wrapping/toroidal behavior (coordinates wrap around edges)
grid = Grid(data=[0] * 100, w=10, h=10, allow_overflow=True)

# Transform element types
int_grid = grid.transform(int)  # Convert str grid to int grid
```

### Accessing Grid Elements

```python
# Get value at point
value = grid.get(point)  # Returns None if out of bounds
value = grid.get(point, default=".")  # With default

# Indexing
value = grid[point]  # Direct access
grid[point] = new_value  # Direct assignment

# Find elements
pos = grid.find("X")  # Find first occurrence
positions = list(grid.findall("X"))  # Find all occurrences

# Check bounds
if grid.inbounds(point):
    # Point is within grid
```

### Wrapping Coordinates (allow_overflow)

The `allow_overflow` parameter enables toroidal/wrapping behavior where coordinates automatically wrap around grid edges using modulo arithmetic. Useful for simulations on infinite grids or problems with wrapping boundaries.

```python
# Set at grid level (applies to all operations)
grid = Grid(data=[0] * 100, w=10, h=10, allow_overflow=True)
grid[Point(12, 5)] += 1  # Wraps to Point(2, 5)
grid[Point(-1, 3)] = 5   # Wraps to Point(9, 3)

# Or override per operation
grid = Grid(data=[0] * 100, w=10, h=10)  # allow_overflow=False by default
value = grid.get(Point(15, 20), allow_overflow=True)  # Wraps to Point(5, 0)
grid.replace(Point(-2, -3), "#", allow_overflow=True)  # Wraps coordinates

# Works with neighbors too
for neighbor_p, neighbor_val, direction in grid.neighbors(
    point,
    allow_overflow=True  # Neighbors wrap around edges
):
    process(neighbor_p, neighbor_val)
```

**Example from Day 14 (Robot Simulation):**
```python
# Robots move on a wrapping grid
w, h = 101, 103
grid = Grid(data=[0] * w * h, w=w, h=h, allow_overflow=True)

for line in self.lines():
    px, py, vx, vy = ints(line, include_sign=True)
    # Calculate position after 100 steps - coordinates automatically wrap
    x = px + vx * 100
    y = py + vy * 100
    grid[Point(x, y)] += 1  # Increments at wrapped position
```

### Iterating Over Grid

```python
# Iterate all cells
for point, value in grid.iter():
    process(point, value)

# Filter by value
for point, value in grid.iter(include="X"):
    # Only cells with value "X"

for point, value in grid.iter(exclude="#"):
    # All cells except "#"

# Filter with function
for point, value in grid.iter(
    include=lambda p, v: v.isdigit(),
    exclude=lambda p, v: p in seen
):
    # Custom filters
```

**Example from Day 10:**
```python
# Transform to int grid and find all trailheads (value 0)
grid = self.grid.transform(int)
paths = [self._score(grid, pos, val) for pos, val in grid.iter(include=0)]
```

### Neighbors and Movement

```python
# Get neighbors (4-directional by default)
for neighbor_p, neighbor_val, direction in grid.neighbors(point):
    process(neighbor_p, neighbor_val)

# Include diagonals (8-directional)
for neighbor_p, neighbor_val, direction in grid.neighbors(point, include_diagonal=True):
    process(neighbor_p, neighbor_val)

# Filter neighbors
for neighbor_p, neighbor_val, direction in grid.neighbors(
    point,
    include=lambda p, v: v != "#",  # Only non-walls
    exclude=lambda p, v: p in visited  # Skip visited
):
    process(neighbor_p, neighbor_val)

# Get specific neighbor
left_val = grid.left(point)
right_val = grid.right(point)
up_val = grid.up(point)
down_val = grid.down(point)
```

**Example from Day 12:**
```python
# Find neighbors in same region
queue.extend([
    neighbor_p
    for neighbor_p, _, _ in self.grid.neighbors(
        point,
        exclude=lambda p, v: p in region or v != value
    )
])
```

### Pathfinding

```python
# Find shortest path (BFS-based)
path = grid.shortest_path(start_point, end_point)
path = grid.shortest_path(start_point, end_point, exclude="#")  # Avoid walls

# Find reachable positions
for point, steps in grid.reachable(
    start_point,
    min_steps=1,
    max_steps=10,
    exclude="#"
):
    print(f"Can reach {point} in {steps} steps")
```

**Example from Day 18:**
```python
grid = Grid(data=["."] * 71 * 71)
for line in bytes_falling:
    x, y = map(int, line.split(","))
    grid[(x, y)] = "#"

path_length = len(grid.shortest_path(Point(0, 0), Point(70, 70), exclude="#")) - 1
```

### Grid Transformations

```python
# Transpose
transposed = grid.transpose()

# Rotate 90 degrees clockwise
rotated = grid.rotate()

# Get rows/columns
rows = grid.rows()  # list[list[T]]
cols = grid.cols()  # list[list[T]]

# Iterate rows/columns
for row in grid.iter_rows():
    for cell in row:
        process(cell)
```

### Walking in Directions

```python
from aoc_utils.point import Direction

# Walk multiple steps in directions
values = list(grid.walk_directions(
    point,
    [Direction.RIGHT] * 3,  # Walk right 3 times
    default=".",
    include_start=True
))
```

**Example from Day 4:**
```python
# Check for "XMAS" pattern in all 8 directions
sum(
    all(expected == actual
        for expected, actual in zip(
            "MAS",
            self.grid.walk_directions(point, [direction] * 3, default=".")
        ))
    for point, _ in self.grid.iter(include="X")
    for direction in Direction
)
```

## Point & Direction

Coordinate system with direction support, neighbor iteration, and distance calculations.

### Point

```python
from aoc_utils.point import Point

# Create point
p = Point(x=5, y=10)
p = Point(3, 4)

# Alternative names
p.row  # Same as p.y
p.col  # Same as p.x

# Arithmetic
p1 + p2  # Add points
p1 - p2  # Subtract points
p + Direction.UP  # Move in direction

# Neighbors
for neighbor in p.neighbors():  # 4 neighbors (up, down, left, right)
    process(neighbor)

for neighbor in p.neighbors(include_diagonal=True):  # 8 neighbors
    process(neighbor)

# With direction info
for neighbor, direction in p.neighbors_with_direction():
    print(f"Neighbor {neighbor} is {direction}")

# Specific neighbors
p.left, p.right, p.up, p.down
p.upper_left, p.upper_right, p.bottom_left, p.bottom_right

# Distance calculations
manhattan = p1.manhattan_distance(p2)
euclidean = p1.euclidean_distance(p2)

# Shoelace formula for polygon area
inner_points = Point.num_inner_points(polygon_vertices)
```

### Direction

```python
from aoc_utils.point import Direction

# Direction enum
Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT
Direction.UPPER_LEFT, Direction.UPPER_RIGHT
Direction.LOWER_LEFT, Direction.LOWER_RIGHT

# Parse from string
d = Direction.from_str("U")  # UP
d = Direction.from_str("NORTH")  # UP
d = Direction.from_str("<")  # LEFT

# Rotation
d.clockwise  # Turn right
d.counter_clockwise  # Turn left
d.clockwise8  # Turn right (8-directional)
d.counter_clockwise8  # Turn left (8-directional)

# Convert to Point offset
offset = Direction.UP.point  # Point(0, -1)

# Multiply for distance
far_point = point + 5 * Direction.RIGHT  # Move 5 spaces right

# Arrow representation
arrow = Direction.UP.arrow  # "↑"

# Iterate all directions
for direction in Direction.dir4():  # 4 cardinal directions
    check(direction)

for direction in Direction.dir8():  # 8 directions
    check(direction)
```

**Example from Day 6:**
```python
dir = Direction.UP
while condition:
    neighbor_pos = pos.neighbor(dir)
    if grid.get(neighbor_pos) == "#":
        dir = dir.clockwise  # Turn right at obstacles
    else:
        pos = neighbor_pos
```

## Helpers

Utility functions for common parsing tasks.

### Extract Integers

```python
from aoc_utils.helpers import ints

# Extract all integers from string
numbers = list(ints("x=42, y=-17, z=100"))  # [42, 17, 100]

# Include signs
numbers = list(ints("x=42, y=-17", include_sign=True))  # [42, -17]
```

## Testing Framework

Set up automated testing with YAML manifests.

### Test Structure

```
day01/
├── solution.py
├── test.py
├── manifest.yaml
└── input.txt
```

### manifest.yaml

```yaml
part1:
  - input: |
      3   4
      4   3
      2   5
      1   3
      3   9
      3   3
    output: 11
    name: "Example 1"

  - input: example2.txt  # Or reference a file
    output: 42

part2:
  - input: |
      test data
    output: 100
```

### test.py

```python
import unittest
from pathlib import Path
from aoc_utils.aoc_test_case import AOCTestCase, ProblemPart
from solution import Solver

class Part1(AOCTestCase):
    _PROBLEM_PART = ProblemPart.PART1
    _SOLVER = Solver
    _DATA_DIR = str(Path(__file__).parent)
    _MANIFEST_PATH = str(Path(__file__).parent / "manifest.yaml")

class Part2(AOCTestCase):
    _PROBLEM_PART = ProblemPart.PART2
    _SOLVER = Solver
    _DATA_DIR = str(Path(__file__).parent)
    _MANIFEST_PATH = str(Path(__file__).parent / "manifest.yaml")

if __name__ == "__main__":
    unittest.main()
```

## Advanced Examples

### Combining Grid + Point + Direction (Day 6 - Guard Patrol)

```python
def walk(self, grid: Grid, pos: Point, dir: Direction) -> Result:
    seen = set()
    while pos not in seen:
        seen.add(pos)
        neighbor_pos = pos.neighbor(dir)
        match grid.get(neighbor_pos):
            case None:
                return Result(seen, False)
            case "#":
                dir = dir.clockwise
            case _:
                pos = neighbor_pos
    return Result(seen, True)
```

### Region Finding with Grid Iteration (Day 12 - Garden Plots)

```python
def _extract_regions(self) -> Iterator[set[Point]]:
    seen = set()
    for region_start, value in self.grid.iter(exclude=lambda p, _: p in seen):
        region = set()
        queue = [region_start]
        while queue:
            point = queue.pop()
            region.add(point)
            queue.extend([
                neighbor_p
                for neighbor_p, _, _ in self.grid.neighbors(
                    point,
                    exclude=lambda p, v: p in region or v != value
                )
            ])
        seen |= region
        yield region
```

### Recursive Pathfinding with Grid.neighbors (Day 10 - Hiking Trails)

```python
def _score(self, grid: Grid[int], pos: Point, val: int) -> list[Point]:
    return (
        [pos] if val == 9
        else [
            point
            for neighbor_pos, neighbor_val, _ in grid.neighbors(pos, include=val + 1)
            for point in self._score(grid, neighbor_pos, neighbor_val)
        ]
    )
```

<!--- advent_readme_stars table --->
## 2024 Results

| Day | Part 1 | Part 2 |
| :---: | :---: | :---: |
| [Day 1](https://adventofcode.com/2024/day/1) | ⭐ | ⭐ |
| [Day 2](https://adventofcode.com/2024/day/2) | ⭐ | ⭐ |
| [Day 3](https://adventofcode.com/2024/day/3) | ⭐ | ⭐ |
| [Day 4](https://adventofcode.com/2024/day/4) | ⭐ | ⭐ |
| [Day 5](https://adventofcode.com/2024/day/5) | ⭐ | ⭐ |
| [Day 6](https://adventofcode.com/2024/day/6) | ⭐ | ⭐ |
| [Day 7](https://adventofcode.com/2024/day/7) | ⭐ | ⭐ |
| [Day 8](https://adventofcode.com/2024/day/8) | ⭐ | ⭐ |
| [Day 9](https://adventofcode.com/2024/day/9) | ⭐ | ⭐ |
| [Day 10](https://adventofcode.com/2024/day/10) | ⭐ | ⭐ |
| [Day 11](https://adventofcode.com/2024/day/11) | ⭐ | ⭐ |
| [Day 12](https://adventofcode.com/2024/day/12) | ⭐ | ⭐ |
| [Day 13](https://adventofcode.com/2024/day/13) | ⭐ | ⭐ |
| [Day 14](https://adventofcode.com/2024/day/14) | ⭐ | ⭐ |
| [Day 15](https://adventofcode.com/2024/day/15) | ⭐ | ⭐ |
| [Day 16](https://adventofcode.com/2024/day/16) | ⭐ | ⭐ |
| [Day 17](https://adventofcode.com/2024/day/17) | ⭐ | ⭐ |
| [Day 18](https://adventofcode.com/2024/day/18) | ⭐ | ⭐ |
| [Day 19](https://adventofcode.com/2024/day/19) | ⭐ | ⭐ |
| [Day 20](https://adventofcode.com/2024/day/20) | ⭐ | ⭐ |
| [Day 23](https://adventofcode.com/2024/day/23) | ⭐ | ⭐ |
| [Day 25](https://adventofcode.com/2024/day/25) | ⭐ |   |
<!--- advent_readme_stars table --->
