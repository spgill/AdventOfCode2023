#! /usr/bin/env python3
### stdlib imports
import enum
import re

### local imports
import utils


class Color(enum.Enum):
    Red = "red"
    Green = "green"
    Blue = "blue"


@utils.part1
def part1(puzzle_input: str):
    # Start by parsing the puzzle input line by line to turn it into workable data
    cube_games: list[list[list[tuple[int, Color]]]] = []
    for line in puzzle_input.strip().splitlines():
        this_game: list[list[tuple[int, Color]]] = []
        for subset in line.split(";"):
            this_hand: list[tuple[int, Color]] = []
            for match in re.findall(r"(\d+) (red|green|blue)", subset):
                this_hand.append((int(match[0]), Color(match[1])))
            this_game.append(this_hand)
        cube_games.append(this_game)

    # These are the conditions set by the puzzle prompt
    bag_contents: dict[Color, int] = {
        Color.Red: 12,
        Color.Green: 13,
        Color.Blue: 14,
    }

    # Now we need to iterate through each game round and figure out which
    # would have been possible given the bag's predefined contents
    valid_game_sum = 0
    for idx, game in enumerate(cube_games):
        game_id = idx + 1
        game_invalid = False

        # We check that no hand in the game pulled out more cubes
        # than exist in the bag
        for hand in game:
            for hand_count, hand_color in hand:
                if hand_count > bag_contents[hand_color]:
                    game_invalid = True

        if not game_invalid:
            valid_game_sum += game_id

    # The answer is the sum of the valid game IDs
    utils.print_answer(valid_game_sum)

    # Pass the parsed puzzle input to the second part
    return cube_games


@utils.part2
def part2(_, cube_games: list[list[list[tuple[int, Color]]]]):
    # We start by iterating through the games again
    game_power_sum = 0
    for game in cube_games:
        # We need to keep track of the number of cubes required per color
        cube_counts: dict[Color, int] = {
            Color.Red: 0,
            Color.Green: 0,
            Color.Blue: 0,
        }

        # Iterate through each hand of the game to find the necessary number of cubes
        for hand in game:
            for hand_count, hand_color in hand:
                cube_counts[hand_color] = max(
                    cube_counts[hand_color], hand_count
                )

        # Multiply these counts together to get the power and add it to the
        # overall sum
        game_power_sum += (
            cube_counts[Color.Red]
            * cube_counts[Color.Green]
            * cube_counts[Color.Blue]
        )

    # The answer is the sum of all game "power"s
    utils.print_answer(game_power_sum)


if __name__ == "__main__":
    utils.start()
