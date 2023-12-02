"""
This module provides helper functions for orchestration Advent of Code puzzle solutions.
"""
### stdlib imports
import copy
import sys
import typing

### vendor imports
import rich
import typer


# Global variables
_quiet_mode: bool = False
_part1_solution_func: typing.Optional[typing.Callable] = None
_part2_solution_func: typing.Optional[typing.Callable] = None
_exec_options: dict[str, typing.Union[str, bool]] = {}


def get_option(key: str) -> typing.Union[str, bool, None]:
    """Get the value of a CLI solution option. If not defined, will return `None`."""
    return _exec_options.get(key, None)


def part1(func: typing.Callable[[str], typing.Any]):
    """
    Decorator to wrap around the solution function for Part 1.

    The first (and only) positional argument is the puzzle input.

    Return value is passed onto the solution function for Part 2.

    Example;
    ```
    @utils.part1
    def solutionOne(data: str):
        answer = math.sqrt(len(data))
        utils.printAnswer(str(answer))
        return answer
    ```
    """
    global _part1_solution_func
    _part1_solution_func = func
    return func


def part2(func: typing.Callable[[str, typing.Any], None]):
    """
    Decorator to wrap around the solution function for Part 2.

    The first positional argument is the puzzle input. The second argument is
    the return value from Part 1's solution function.

    Example;
    ```
    @utils.part2
    def solutionTwo(data: str, previous: int):
        answer = previous * math.pi
        utils.printAnswer(str(answer))
    ```
    """
    global _part2_solution_func
    _part2_solution_func = func
    return func


def _cli(
    input: typer.FileBinaryRead = typer.Argument(
        ..., help="Puzzle input file. Use '-' to read from STDIN."
    ),
    quiet: bool = typer.Option(
        not sys.stdout.isatty(),
        "-q",
        "--quiet",
        help="Enables quiet mode. Suppresses messages and fancy formatting. Warnings and errors will still be written to STDERR. Automatically enabled if stdout is not a tty.",
    ),
    skip_part2: bool = typer.Option(
        False,
        "--skip-part-2/",
        "-s/",
        help="Skip execution of the solution for part 2. Part 1 will ALWAYS be executed.",
    ),
    option: list[str] = typer.Option(
        [],
        "-o",
        "--option",
        help="Provide the solution with an execution option. These options may enable extra output (like ASCII displays) or perhaps experimental behaviors. Syntax is '--option KEY=VALUE' or '--option FLAG' for a boolean flag. Available options should be documented in the solution script itself. Can be specified multiple times to set more than one option.",
    ),
):
    """Internal function for executing the puzzle solutions."""
    # First we need to read and decode the puzzle input.
    input_data: str = input.read().decode()

    # Next, we should parse out any key=value options
    for entry in option:
        entry_split = entry.split("=")
        key = entry_split[0]
        value = True if len(entry_split) == 1 else entry_split[1]
        _exec_options[key] = value

    global _quiet_mode, _part1_solution_func, _part2_solution_func
    _quiet_mode = quiet

    # Run the part 1 solution
    part1_result: typing.Any = None
    if _part1_solution_func is None:
        print_error("No solution function was defined for Part 1!")
        exit(1)
    else:
        print_message("Part 1 solution is executing...")
        part1_result = _part1_solution_func(copy.copy(input_data))

    # Run the part 2 solution if desired and it exists
    if not skip_part2:
        print_message("")
        if _part2_solution_func is None:
            print_warning("No solution function was defined for Part 2!")
        else:
            print_message("Part 2 solution is executing...")
            _part2_solution_func(copy.copy(input_data), part1_result)


def start():
    """This function will start the Typer CLI."""
    typer.run(_cli)


def print_message(message: str) -> None:
    if not _quiet_mode:
        rich.print(message)


def print_answer(value: typing.Any) -> None:
    """Print the solution to Part `part` of the puzzle"""
    if _quiet_mode:
        print(value)
    else:
        rich.print(f"[green]Answer:[/] {value}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    rich.print(f"[yellow italic]Warning: {message}[/]", file=sys.stderr)


def print_computation_warning() -> None:
    """Print a warning about computation time."""
    print_warning("It may take awhile to compute answers...")


def print_computation_warning_with_prompt() -> None:
    """
    Print a warning about computation time,
    prompting the user to continue.
    """
    if not _quiet_mode:
        typer.confirm(
            "[yellow italic]Warning: It may take a very long while to compute answers. Continue?[/]",
            default=True,
            abort=True,
        )


def print_error(message: str) -> None:
    """Print an error in red and abort execution"""
    rich.print(f"[red]Error:[/] {message}", file=sys.stderr)
