from typing import Any, Literal, Union

from rich import box
from rich.align import Align
from rich.box import Box
from rich.console import Console, Group
from rich.padding import Padding as Margin  # Funny enough, padding is margin here
from rich.panel import Panel

console: Console = Console()

ALL_BOXES: dict[str, Box] = {
    "ascii": box.ASCII,
    "ascii2": box.ASCII2,
    "ascii_double_head": box.ASCII_DOUBLE_HEAD,
    "square": box.SQUARE,
    "square_double_head": box.SQUARE_DOUBLE_HEAD,
    "minimal": box.MINIMAL,  # basically hidden box
    "minimal_heavy_head": box.MINIMAL_HEAVY_HEAD,  # REMOVE: same as above
    "minimal_double_head": box.MINIMAL_DOUBLE_HEAD,  # REMOVE: same as above
    "simple": box.SIMPLE,  # REMOVE: same as above
    "simple_head": box.SIMPLE_HEAD,  # REMOVE: same as above
    "simple_heavy": box.SIMPLE_HEAVY,  # REMOVE: same as above
    "horizontals": box.HORIZONTALS,
    "rounded": box.ROUNDED,
    "heavy": box.HEAVY,
    "heavy_edge": box.HEAVY_EDGE,  # REMOVE: same as above
    "heavy_head": box.HEAVY_HEAD,  # REMOVE: does not make sense
    "double": box.DOUBLE,
    "double_edge": box.DOUBLE_EDGE,  # REMOVE: same as above
    "markdown": box.MARKDOWN,  # REMOVE: does not make sense
}


def parse_size(size: Union[int, tuple[int, ...]], instance: str) -> tuple:
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


def make_margin(margin: Union[int, tuple[int]]) -> tuple:
    return parse_size(margin, "margin")


def make_padding(padding: Union[int, tuple[int]]) -> tuple:
    return parse_size(padding, "padding")


POSITION_TYPES = ["left", "center", "right"]


def boxen(
    *text: Any,
    color: str = "white",
    style: str = "rounded",
    padding: Union[int, tuple[int]] = 0,
    margin: Union[int, tuple[int]] = 0,
    text_alignment: Literal["left", "center", "right"] = "center",
    box_alignment: Literal["left", "center", "right"] = "left",
    title: str = None,
    title_alignment: Literal["left", "center", "right"] = "left",
    subtitle: str = None,
    subtitle_alignment: Literal["left", "center", "right"] = "left",
    fullwidth: bool = False,
):
    """
    It takes a bunch of arguments,
    validates them, and then returns a string of the rendered box

    :param: *text: Any
    :type: Any
    :param color: The color of the box, defaults to white
    :type color: str (optional)
    :param style: The style of the box. Can be one of the following:, defaults to rounded
    :type style: str (optional)
    :param padding: The padding between the text and the box, defaults to 0
    :type padding: Union[int, tuple[int]] (optional)
    :param margin: The margin around the box, defaults to 0
    :type margin: Union[int, tuple[int]] (optional)
    :param align: The alignment of the text inside the box, defaults to center
    :type align: Literal["left", "center", "right"] (optional)
    :param box_align: The alignment of the box, defaults to left
    :type box_align: Literal["left", "center", "right"] (optional)
    :param title: The title of the box
    :type title: str
    :param title_alignment: The alignment of the title, defaults to left
    :type title_alignment: Literal["left", "center", "right"] (optional)
    :param subtitle: str = None,
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
        if (
            style
            and not isinstance(style, str)
            and style.lower() not in ALL_BOXES.keys()
        ):
            raise ValueError(f"style must be one of {ALL_BOXES.keys()}")
        if (
            text_alignment
            and not isinstance(text_alignment, str)
            and text_alignment not in POSITION_TYPES
        ):
            raise ValueError(f"text alignment must be one of {POSITION_TYPES}")
        if (
            box_alignment
            and not isinstance(box_alignment, str)
            and box_alignment not in POSITION_TYPES
        ):
            raise ValueError(f"box alignment must be one of {POSITION_TYPES}")
        if (
            title_alignment
            and not isinstance(title_alignment, str)
            or title_alignment not in POSITION_TYPES
        ):
            raise ValueError(f"title alignment must be one of {POSITION_TYPES}")
        if (
            subtitle_alignment
            and not isinstance(subtitle_alignment, str)
            or subtitle_alignment not in POSITION_TYPES
        ):
            raise ValueError(f"subtitle alignment must be one of {POSITION_TYPES}")
        if fullwidth and not isinstance(fullwidth, bool):
            raise TypeError("fullwidth must be either True or False")

    validate_args()

    def make_panel() -> Panel:
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
        console.print(make_panel())

    return capture.get()
