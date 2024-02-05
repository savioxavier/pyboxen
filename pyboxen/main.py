"""
Package boxen allows you to create customizable boxes in the terminal

It is built on top of Rich, and is fully compatible with most Rich styling syntax and Rich renderables
"""

from typing import Any, Literal, Union, Dict, Tuple

from rich import box
from rich.align import Align
from rich.box import Box
from rich.console import Console, Group
from rich.padding import Padding as Margin  # Funny enough, padding is margin here
from rich.panel import Panel

console: Console = Console()

ALL_BOXES: Dict[str, Box] = {
    "ascii": box.ASCII,
    "ascii2": box.ASCII2,
    "ascii_double_head": box.ASCII_DOUBLE_HEAD,
    "square": box.SQUARE,
    "square_double_head": box.SQUARE_DOUBLE_HEAD,
    "minimal": box.MINIMAL,  # basically hidden box
    "horizontals": box.HORIZONTALS,
    "rounded": box.ROUNDED,
    "heavy": box.HEAVY,
    "double": box.DOUBLE,
}


def parse_size(size: Union[int, Tuple[int, ...]], instance: str) -> Tuple:
    if isinstance(size, tuple) and len(size) not in (2, 4):
        raise ValueError(
            f"{instance} tuples must have either a total of 2 or 4 elements in it"
        )
    elif isinstance(size, tuple) and len(size) == 2:
        top = bottom = size[0]
        right = left = size[1]
    elif isinstance(size, tuple) and len(size) == 4:
        top = size[0]
        right = size[1]
        bottom = size[2]
        left = size[3]
    elif isinstance(size, int):
        # If only an int is specified, then the left and right
        # size values will be multiplied by 3 for a better look
        # and to mimic the behavior of the npm package boxen
        # Previously, it used to be just the number of characters on the left and right
        # ie, if padding is int and set to n, then:
        #   top = n lines
        #   right = n characters
        #   bottom = n lines
        #   left = n characters
        # This looked weird in the terminal and has been modified below
        # NOTE: This behaviour can be overridden by setting the values as tuple instead of int
        # as this is applicable only for ints

        top, right, bottom, left = size, size * 3, size, size * 3
    else:
        raise TypeError(f"{instance} must be either int or tuple of ints")

    return (top, right, bottom, left)


def make_margin(margin: Union[int, Tuple[int]]) -> Tuple:
    return parse_size(margin, "margin")


def make_padding(padding: Union[int, Tuple[int]]) -> Tuple:
    return parse_size(padding, "padding")


POSITION_TYPES = ["left", "center", "right"]


def boxen(
    *text: Any,
    color: str = "white",
    style: Literal[
        "ascii",
        "ascii2",
        "ascii_double_head",
        "square",
        "square_double_head",
        "minimal",
        "horizontals",
        "rounded",
        "heavy",
        "double",
    ] = "rounded",
    padding: Union[int, Tuple[int]] = 0,
    margin: Union[int, Tuple[int]] = 0,
    text_alignment: Literal["left", "center", "right"] = "center",
    box_alignment: Literal["left", "center", "right"] = "left",
    title: str = None,
    title_alignment: Literal["left", "center", "right"] = "left",
    subtitle: str = None,
    subtitle_alignment: Literal["left", "center", "right"] = "left",
    fullwidth: bool = False,
):
    """
    Create a customizable box to be displayed in the terminal

    :param: *text: A variable set of strings to display in the box, or any other Rich renderable(s)
    :type: Any
    :param color: The color of the box in color or hex code starting with #, defaults to white
    :type color: str (optional)
    :param style: The style of the box, defaults to rounded
    :type style: str (optional)
    :param padding: The padding between the text and the box in int or tuple of ints, defaults to 0
    :type padding: Union[int, Tuple[int]] (optional)
    :param margin: The margin around the box in int or tuple of ints, defaults to 0
    :type margin: Union[int, Tuple[int]] (optional)
    :param text_alignment: The alignment of the text inside the box, defaults to center
    :type text_alignment: Literal["left", "center", "right"] (optional)
    :param box_alignment: The alignment of the box in the terminal, defaults to left
    :type box_alignment: Literal["left", "center", "right"] (optional)
    :param title: The title of the box, displayed on the top of the box, if provided
    :type title: str
    :param title_alignment: The alignment of the title, defaults to left
    :type title_alignment: Literal["left", "center", "right"] (optional)
    :param subtitle: str The subtitle of the box, displayed on the bottom of the box, if provided
    :type subtitle: str
    :param subtitle_alignment: The alignment of the subtitle, defaults to left
    :type subtitle_alignment: Literal["left", "center", "right"] (optional)
    :param fullwidth: If True, the box will expand to fill the entire terminal width, defaults to False
    :type fullwidth: bool (optional)
    :return: A string
    """

    def validate_args():
        # padding and margin errors are handled in their respective functions
        # so we don't specify them here

        # we don't check for text because text can be any Rich renderable, including str

        if color and not isinstance(color, str):
            raise TypeError("color must be a string")
        if title and not isinstance(title, str):
            raise TypeError("title must be a string")
        if subtitle and not isinstance(subtitle, str):
            raise TypeError("subtitle must be a string")
        if style and (
            not isinstance(style, str) or style.lower() not in ALL_BOXES.keys()
        ):
            raise ValueError(f"style must be one of {list(ALL_BOXES.keys())}")
        if text_alignment and (
            not isinstance(text_alignment, str) or text_alignment not in POSITION_TYPES
        ):
            raise ValueError(f"text alignment must be one of {POSITION_TYPES}")
        if box_alignment and (
            not isinstance(box_alignment, str) or box_alignment not in POSITION_TYPES
        ):
            raise ValueError(f"box alignment must be one of {POSITION_TYPES}")
        if title_alignment and (
            not isinstance(title_alignment, str)
            or title_alignment not in POSITION_TYPES
        ):
            raise ValueError(f"title alignment must be one of {POSITION_TYPES}")
        if subtitle_alignment and (
            not isinstance(subtitle_alignment, str)
            or subtitle_alignment not in POSITION_TYPES
        ):
            raise ValueError(f"subtitle alignment must be one of {POSITION_TYPES}")
        if fullwidth and not isinstance(fullwidth, bool):
            raise TypeError("fullwidth must be either True or False")

    validate_args()

    def build_box() -> Panel:
        return Align(
            Margin(
                Panel(
                    renderable=Align(Group(*text), align=text_alignment),
                    box=ALL_BOXES[style.lower()],
                    border_style=color,
                    expand=fullwidth,
                    padding=make_padding(padding),
                    title=title,
                    title_align=title_alignment,
                    subtitle=subtitle,
                    subtitle_align=subtitle_alignment,
                    highlight=False,
                ),
                pad=make_margin(margin),
            ),
            align=box_alignment,
        )

    with console.capture() as capture:
        console.print(build_box())

    return capture.get()
