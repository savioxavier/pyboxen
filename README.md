# pyboxen
<!-- markdownlint-disable MD010 MD033 MD001 -->

> **Create beautiful boxes in the terminal using Python**

This package is a Python "port" of the popular NPM package [boxen](https://github.com/sindresorhus/boxen/).

It's built on top of [Rich](https://github.com/Textualize/rich/), and features an API that would be familiar to the users of the NPM boxen package.

## 🛠️ Install

Using [pip](https://pypi.org/)

```text
pip install boxen
```

---

## 🔗 Usage

- Simplest of simple boxes

```py
from boxen import boxen

print(boxen("Python is cool!"))
```
![image](https://user-images.githubusercontent.com/38729705/198232802-e41575c6-abd6-416d-9ba6-d1b1c31a2660.png)

- Define options

```py
from boxen import boxen

print(
    boxen(
        "Python is cool!",
        padding=1,
        margin=1,
        color="cyan",
    )
)
```
![image](https://user-images.githubusercontent.com/38729705/198233490-52feeeba-efd3-4fe4-93cf-641d0f58fbf4.png)

- Multiple texts and [Rich Renderables](https://github.com/Textualize/rich#rich-library)

> You can even use Rich's special color style syntax for the text, title and subtitle as well
>
> Example: `[red]Hello[/red] [bold italic]World[/]`

```py
from boxen import boxen

# Multiple texts

print(
    boxen(
        "Python is cool!",
        "Yeah it totally is!",
        "I [red]:heart:[/red]  [yellow bold]Python[/]!",  # You can even use Rich syntax here too!
        padding=1,
        margin=1,
        color="cyan",
    )
)

# Rich renderables, with a mix of strings and renderables

from rich.table import Table

table = Table(show_header=True, header_style="bold magenta")

table.add_column("Date", style="dim", width=12)
table.add_column("Title")
table.add_column("Production Budget", justify="right")
table.add_column("Box Office", justify="right")
table.add_row(
    "Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$275,000,000", "$375,126,118"
)
table.add_row(
    "May 25, 2018",
    "[red]Solo[/red]: A Star Wars Story",
    "$275,000,000",
    "$393,151,347",
)
table.add_row(
    "Dec 15, 2017",
    "Star Wars Ep. VIII: The Last Jedi",
    "$262,000,000",
    "[bold]$1,332,539,889[/bold]",
)

print(
    boxen(
        "Python is cool!",
        table
    )
)
```
![image](https://user-images.githubusercontent.com/38729705/198234218-0a4ccfd8-a858-4f84-a99d-f804b926f684.png)

- Title and subtitles

```py
from boxen import boxen

print(
    boxen(
        "Titles and subtitles!",
        title="Hello, [black on cyan] World [/]",
        subtitle="Cool subtitle goes here",
        subtitle_alignment="center",
        color="yellow",
        padding=1,
    )
)
```
---

## 🔮 API

### `boxen(*text, **kwargs)`

#### text

A variable (infinite) amount of text strings or [Rich Renderables](https://github.com/Textualize/rich#rich-library), or a mix of both.

#### kwargs

Customize options for the box

Available options include:

```py
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
```

#### color

The color of the box in color or hex code starting with #, defaults to white

#### style

The style of the box, defaults to rounded

#### padding

The padding between the text and the box in int or tuple of ints, defaults to 0

#### margin

The margin around the box in int or tuple of ints, defaults to 0

#### text_alignment

The alignment of the text inside the box, defaults to center

#### box_alignment

The alignment of the box in the terminal, defaults to left

#### title

The title of the box, displayed on the top of the box, if provided

#### title_alignment

The alignment of the title, defaults to left

#### subtitle

The subtitle of the box, displayed on the bottom of the box, if provided

#### subtitle_alignment

The alignment of the subtitle, defaults to left

#### fullwidth

If True, the box will expand to fill the entire terminal width, defaults to False

> **Note**
> `padding` and `margin` attributes can be either an int, a tuple of ints (with a total of either 2 elements or 4 elements)
> Example:
>
> `2` - all of top, right, bottom, left
>
> `(2, 4)` - (top = bottom, right = left)
>
> `(2, 4, 6, 8)` - (top, right, bottom, left)

---

## ❤️ Support

You can support further development of this project by **giving it a 🌟** and help me make even better stuff in the future by **buying me a ☕**

<a href="https://www.buymeacoffee.com/savioxavier">
<img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" height="50px">
</a>

<br>

**Also, if you liked this repo, consider checking out my other projects, that would be real cool!**

---

## 💫 Attributions and special thanks

- [boxen](https://github.com/sindresorhus/boxen/) - the NPM package I was inspired from
- [rich](https://github.com/Textualize/rich) - for making such an incredibly powerful text customization tool
