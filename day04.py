#! /usr/bin/env python3
### stdlib imports
import re

### local imports
import utils


@utils.part1
def part1(puzzle_input: str):
    # Begin by parsing the puzzle input into a data structure representing
    # the scratchcards
    scratchcards: list[tuple[set[int], set[int]]] = []
    for line in puzzle_input.strip().splitlines():
        match = re.match(r"^Card[ \d]+: (.*?) \| (.*?)$", line)
        assert match is not None, "Error parsing line in puzzle input"

        winning_numbers = set(
            int(s) for s in re.findall(r"(\d+)", match.group(1))
        )
        drawn_numbers = set(
            int(s) for s in re.findall(r"(\d+)", match.group(2))
        )
        scratchcards.append((winning_numbers, drawn_numbers))

    # Now we iterate through the parsed numbers, and find intersection between
    # winning numbers and drawn numbers. The number of matches is used to tally
    # up a total of points
    points = 0
    for winning_numbers, drawn_numbers in scratchcards:
        matches = len(winning_numbers.intersection(drawn_numbers))
        if matches > 0:
            points += 2 ** (matches - 1)

    # The total number of points is the final answer
    utils.print_answer(points)

    # Pass the parsed scratchcard numbers to part 2
    return scratchcards


@utils.part2
def part2(_, scratchcards: list[tuple[set[int], set[int]]]):
    # For this part, we'll need to track "copies" that we've received of each
    # scratchcard. Every scratchcard is initialized as 1 copy.
    copies: dict[int, int] = {i: 1 for i in range(len(scratchcards))}

    # Now we iterate through the scratchcards and the number of matches dictates
    # the number of copies we are given
    for i, (winning_numbers, drawn_numbers) in enumerate(scratchcards):
        copies_of_this_card = copies[i]
        matches = len(winning_numbers.intersection(drawn_numbers))
        for j in range(matches):
            copies[i + j + 1] += copies_of_this_card

    # The answer to this part is the total count of cards, including all copies
    utils.print_answer(sum(count for _, count in copies.items()))


if __name__ == "__main__":
    utils.start()
