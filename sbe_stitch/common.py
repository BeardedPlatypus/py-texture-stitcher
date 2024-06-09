from typing import Optional, Tuple, Union, TypeAlias
from rich import print
from rich.padding import Padding


Pad: TypeAlias = Union[int, Tuple[int, int], Tuple[int, int, int, int]]


def _print_msg(suffix: str, msg: str, padding: Optional[Pad]) -> None:
    msg = f"{suffix} {msg}"
    if padding:
        msg = Padding(msg, padding)
    print(msg)


def info(msg: str, padding: Optional[Pad]=None) -> None:
    _print_msg("[bold steel_blue1]Info:[/bold steel_blue1]", msg, padding)


def warning(msg: str, padding: Optional[Pad]=None) -> None:
    _print_msg("[bold orange1]Warning:[/bold orange1]", msg, padding)


def error(msg: str, padding: Optional[Pad]=None) -> None:
    _print_msg("[bold bright_red]Error:[/bold bright_red]", msg, padding)


def success(msg: str, padding: Optional[Pad]=None) -> None:
    _print_msg("[bold chartreuse1]Success:[/bold chartreuse1]", msg, padding)
