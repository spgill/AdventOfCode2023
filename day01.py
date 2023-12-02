#! /usr/bin/env python3
### stdlib imports
import re

### local imports
import utils


@utils.part1
def part1(puzzleInput: str):
    # Split the input into lines
    lines = puzzleInput.strip().splitlines()

    sum = 0

    # Iterate through each line, extract the relevant digits, and add them
    # to the sum
    for line in lines:
        digits = re.sub(r"\D", "", line)
        if not digits:
            continue
        value = int(digits[0] + digits[-1])
        sum += value

    # The answer is the sum
    utils.print_answer(sum)

    # Pass lines to the next part
    return lines


digit_spellings: dict[str, str] = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


@utils.part2
def part2(_, lines: list[str]):
    # Iterate through each line of the puzzle input and modify the lines
    # to expose the spelled out digits.
    modified_lines: list[str] = []
    for line in lines:
        # We will be substituting spelled out digits for their actual number values.
        # However it's not so simple as it first appears, because the spelled out
        # digits may have characters that overlap e.g., "eightwo" is 8 and 2 sharing
        # the letter "t" between them. One solution is to replace the word
        # with the decimal value both prefixed and suffixed with the original word
        # this way no adjascent words are swallowed .e.g., "eightwo" becomes
        # "eight8eightwo2two" which can then be parsed using the same logic from
        # the part 1 solution.
        for spelling, digit in digit_spellings.items():
            line = re.sub(f"({spelling})", r"\g<1>" + digit + r"\g<1>", line)

        modified_lines.append(line)

    # We can pass these modified lines straight back to part 1 for solving
    part1("\n".join(modified_lines))


if __name__ == "__main__":
    utils.start()
