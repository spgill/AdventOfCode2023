#! /usr/bin/env python3
### stdlib imports
import enum
import math
import re
import typing

### vendor imports
import more_itertools

### local imports
import utils


class SeedMapName(enum.Enum):
    Seed2Soil = "seed-to-soil"
    Soil2Fertilizer = "soil-to-fertilizer"
    Fertilizer2Water = "fertilizer-to-water"
    Water2Light = "water-to-light"
    Light2Temperature = "light-to-temperature"
    Temperature2Humidity = "temperature-to-humidity"
    Humidity2Location = "humidity-to-location"


_cached_values: dict[int, int] = {}


def find_lowest_mapped_value(
    seed_values: typing.Iterable[int], seed_maps: list[list[tuple[int, ...]]]
) -> int:
    # For each seed, run the seed number through all of the seed map ranges
    # to determine the final location number. We need to track the lowest
    # location value that is found.
    lowest_value: typing.Union[float, int] = math.inf
    for start_value in seed_values:
        current_value: int = 0

        if start_value in _cached_values:
            current_value = _cached_values[start_value]
        else:
            current_value = start_value
            for map_ranges in seed_maps:
                for destination_start, source_start, length in map_ranges:
                    source_end = source_start + length
                    if source_start <= current_value <= source_end:
                        current_value = (
                            current_value - source_start
                        ) + destination_start
                        break

            _cached_values[start_value] = current_value

        lowest_value = min(lowest_value, current_value)

    return int(lowest_value)


@utils.part1
def part1(puzzle_input: str):
    # We'll start extracting the seed numbers from the puzzle input.
    seeds = [
        int(m)
        for m in re.findall(r"(\d+)", puzzle_input.strip().splitlines()[0])
    ]

    # Next we need to extract all of the maps from the number maps from the
    # puzzle input
    seed_maps: dict[SeedMapName, list[tuple[int, ...]]] = {}
    for match in re.finditer(
        r"([\w-]+) map:\n((?:[\d ]+\n)+)", puzzle_input.strip()
    ):
        map_name = SeedMapName(match.group(1))
        seed_maps[map_name] = []
        for line in match.group(2).strip().splitlines():
            seed_maps[map_name].append(
                tuple(int(n) for n in re.findall(r"(\d+)", line))
            )

    # Now we need to organize the seed maps into a list by their proper order.
    # Not strictly necessary because it seems that all puzzle inputs order this
    # correctly in the first place, but I like to be thorough :)
    ordered_seed_maps = [
        seed_maps[SeedMapName.Seed2Soil],
        seed_maps[SeedMapName.Soil2Fertilizer],
        seed_maps[SeedMapName.Fertilizer2Water],
        seed_maps[SeedMapName.Water2Light],
        seed_maps[SeedMapName.Light2Temperature],
        seed_maps[SeedMapName.Temperature2Humidity],
        seed_maps[SeedMapName.Humidity2Location],
    ]

    # The answer is the lowest mapped location value from the seed inputs
    utils.print_answer(find_lowest_mapped_value(seeds, ordered_seed_maps))

    # Pass the seeds and seed maps onto part 2
    return (seeds, ordered_seed_maps)


# I'm not attempting part 2 for now


if __name__ == "__main__":
    utils.start()
