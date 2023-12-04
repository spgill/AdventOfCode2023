#! /usr/bin/env python3
### stdlib imports
import re
import typing

### local imports
import utils


def contains_symbol(c: str) -> bool:
    return bool(re.search(r"[^\w.\n]", c))


def get_adjacent_chars(
    grid: list[str], origin: tuple[int, int], length: int
) -> typing.Generator[tuple[str, tuple[int, int]], None, None]:
    line_length = len(grid[0])

    x_origin, y_origin = origin

    x_start = max(origin[0] - 1, 0)
    x_end = min(origin[0] + length, line_length - 1)

    # Yield characters from the previous row
    if y_origin > 0:
        for x in range(x_start, x_end + 1):
            yield (grid[y_origin - 1][x], (x, y_origin - 1))

    # Yield characters from the current row
    x_prefix = x_origin - 1
    if x_prefix >= 0:
        yield (grid[y_origin][x_prefix], (x_prefix, y_origin))

    x_suffix = x_origin + length
    if x_suffix <= (line_length - 1):
        yield (grid[y_origin][x_suffix], (x_suffix, y_origin))

    # Yield characters from the next row
    if y_origin < (len(grid) - 1):
        for x in range(x_start, x_end + 1):
            yield (grid[y_origin + 1][x], (x, y_origin + 1))


@utils.part1
def part1(puzzle_input: str):
    sum = 0

    # Start by splitting the schematic into lines to approximate a cartesian grid
    schematic_grid = puzzle_input.strip().splitlines()

    # Now iterate through each line and find all numbers on the line
    for y, row in enumerate(schematic_grid):
        for match_obj in re.finditer(r"(\d+)", row):
            x = match_obj.start(1)
            match = match_obj.group(1)
            number = int(match)

            adjacent_chars = "".join(
                a[0]
                for a in get_adjacent_chars(schematic_grid, (x, y), len(match))
            )

            # If the adjacent characters contain a symbol, add this number
            # to the running sum
            if contains_symbol(adjacent_chars):
                sum += number

    # The answer is the sum of all identified numbers
    utils.print_answer(sum)

    # Pass the grid onto part 2
    return schematic_grid


@utils.part2
def part2(_, schematic_grid: list[str]):
    # We need to iterate through the same matches we found in part 1, and then
    # find which of them share an asterisk character
    asterisks: dict[tuple[int, int], list[int]] = {}
    for y, row in enumerate(schematic_grid):
        for match_obj in re.finditer(r"(\d+)", row):
            x = match_obj.start(1)
            match = match_obj.group(1)
            number = int(match)

            adjacent_chars = get_adjacent_chars(
                schematic_grid, (x, y), len(match)
            )

            for char, coords in adjacent_chars:
                if char == "*":
                    if coords not in asterisks:
                        asterisks[coords] = []
                    asterisks[coords].append(number)

    # Now we iterate through asterisks that were identified, and if there were
    # exactly two overlapping numbers, we multiple them and add the product
    # to the running sum
    ratio_sum = 0
    for coord, neighbors in asterisks.items():
        if len(neighbors) == 2:
            ratio_sum += neighbors[0] * neighbors[1]

    utils.print_answer(ratio_sum)


if __name__ == "__main__":
    utils.start()
