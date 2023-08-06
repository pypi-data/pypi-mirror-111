"""
pytermgui.widgets.extra
------------------------
author: bczsalba


This submodule provides some extra widgets. The biggest difference
between these and the ones in .base is that these either fully rely on,
or at least partially use the classes provided in .base.
"""

# these classes will have to have more than 7 attributes mostly.
# pylint: disable=too-many-instance-attributes

from typing import Optional, Callable, Iterator, Union, Any

from .base import (
    Container,
    Label,
    Widget,
    Button,
)

from .styles import (
    default_foreground,
    default_background,
    MarkupFormatter,
    apply_markup,
    StyleType,
    CharType,
)
from ..input import keys
from ..ansi_interface import foreground
from ..helpers import real_length, strip_ansi


def _focus(button: Button, obj: Widget) -> None:
    """Select object

    This is a function to avoid usage of unnamed lambdas."""

    obj.focus()


class ColorPicker(Container):
    """A Container that shows the 256 color table"""

    serialized = Widget.serialized + ["grid_cols"]

    def __init__(self, grid_cols: int = 8) -> None:
        """Initialize object, set width"""

        super().__init__()

        self.grid_cols = grid_cols
        self.forced_width = self.grid_cols * 4 - 1 + self.sidelength
        self.width = self.forced_width

    def get_lines(self) -> list[str]:
        """Get color table lines"""

        chars = self.get_char("border")
        assert isinstance(chars, list)
        left_border, _, right_border, _ = chars

        lines = super().get_lines()
        last_line = lines.pop()

        for line in range(256 // self.grid_cols):
            buff = left_border

            for num in range(self.grid_cols):
                col = str(line * self.grid_cols + num)
                if col == "0":
                    buff += "    "
                    continue

                buff += foreground(f"{col:>3}", col) + " "

            buff = buff[:-1]
            lines.append(buff + "" + right_border)

        lines.append(last_line)
        return lines

    def debug(self) -> str:
        """Return identifiable information about object"""

        return f"ColorPicker(grid_cols={self.grid_cols})"


class Splitter(Container):
    """A Container-like object that allows stacking Widgets horizontally"""

    chars: dict[str, CharType] = {"separator": " | "}

    styles: dict[str, StyleType] = {
        "separator": apply_markup,
    }

    def __init__(self, *elements: Optional[tuple[Widget, ...]]) -> None:
        """Initialize Splitter, add given elements to it"""

        super().__init__()

        self.widths = None

        for widget in elements:
            self += widget

    def get_lines(self) -> str:
        """Get lines of all objects"""

        lines = []
        separator = self.get_char("separator")
        widget_lines = [widget.get_lines() for widget in self._widgets]

        for horizontal in zip(*widget_lines):
            lines.append(separator.join(horizontal))

        return lines


class ProgressBar(Widget):
    """A widget showing Progress"""

    chars: dict[str, CharType] = {
        "fill": ["#"],
        "delimiter": ["[ ", " ]"],
    }

    styles: dict[str, StyleType] = {
        "fill": apply_markup,
        "delimiter": apply_markup,
    }

    def __init__(self, progress_function: Callable[[], float]) -> None:
        """Initialize object"""

        super().__init__()
        self.progress_function = progress_function

    def get_lines(self) -> list[str]:
        """Get lines of object"""

        delimiter_style = self.get_style("delimiter")
        fill_style = self.get_style("fill")

        delimiter_chars = self.get_char("delimiter")
        fill_char = self.get_char("fill")[0]

        start, end = [delimiter_style(char) for char in delimiter_chars]
        progress_float = min(self.progress_function(), 1.0)

        total = self.width - real_length(start + end)
        progress = int(total * progress_float) + 1
        middle = fill_style(progress * fill_char)

        line = start + middle
        return [line + (self.width - real_length(line + end)) * " " + end]

    def debug(self) -> str:
        """Return identifiable information about object"""

        return f"ProgressBar(progress_function={self.progress_function})"


class ListView(Widget):
    """Allow selection from a list of options"""

    LAYOUT_HORIZONTAL = 0
    LAYOUT_VERTICAL = 1

    styles: dict[str, StyleType] = {
        "delimiter": apply_markup,
        "options": apply_markup,
        "highlight": default_background,
    }

    chars: dict[str, CharType] = {"delimiter": ["< ", " >"]}

    click_callback: Callable[[Widget], Any] = _focus

    serialized = Widget.serialized + [
        "*options",
        "padding",
        "layout",
        "align",
    ]

    def __init__(
        self,
        options: Optional[list[str]] = None,
        layout: int = LAYOUT_VERTICAL,
        align: int = Label.ALIGN_CENTER,
        padding: int = 0,
    ) -> None:
        """Initialize object"""

        super().__init__()

        if options is None:
            options = []

        self.padding = padding
        self.options = options
        self.layout = layout
        self.align = align
        self._donor_label = Label(align=self.align)
        self.height = len(self.options)

        self.is_selectable = True
        self.selectables_length = len(options)

    def get_lines(self) -> list[str]:
        """Get lines to represent object"""

        def _find_start(text: str) -> int:
            """Find first non-whitespace in string"""

            for i, char in enumerate(strip_ansi(text)):
                if not char == " ":
                    return i

            return -1

        lines = []

        options_style = self.get_style("options")
        highlight_style = self.get_style("highlight")
        delimiter_style = self.get_style("delimiter")

        chars = self.get_char("delimiter")
        start, end = [delimiter_style(char) for char in chars]

        if self.layout is ListView.LAYOUT_HORIZONTAL:
            pass

        elif self.layout is ListView.LAYOUT_VERTICAL:
            label = self._donor_label
            label.align = self.align
            label.padding = self.padding
            label.width = self.width

            for i, opt in enumerate(self.options):
                value = [start, options_style(opt), end]

                # highlight_style needs to be applied to all widgets in value
                if self._is_focused and i == self.selected_index:
                    label.value = "".join(highlight_style(widget) for widget in value)

                else:
                    label.value = "".join(value)

                for line in label.get_lines():
                    lines.append(line)

                    posx, posy = self.pos
                    x_start_offset = _find_start(line) + 1
                    self.buttons = [
                        Button(
                            start=(posx + self.padding + x_start_offset, posy - 1),
                            end=(
                                posx
                                + self.padding
                                + x_start_offset
                                - 1
                                + real_length(label.value),
                                posy + i - 1,
                            ),
                            callback=self.click_callback,
                        )
                    ]

                # print(self.buttons[-1].start, self.buttons[-1].end)

        return lines

    def get_layout_string(self) -> str:
        """Get layout string"""

        if self.layout is ListView.LAYOUT_HORIZONTAL:
            layout = "LAYOUT_HORIZONTAL"
        elif self.layout is ListView.LAYOUT_VERTICAL:
            layout = "LAYOUT_VERTICAL"

        return "ListView." + layout

    def debug(self) -> str:
        """Return identifiable information about object"""

        return (
            "ListView("
            + f"options={self.options}, "
            + f"layout={self.get_layout_string()}, "
            + f"align={self._donor_label.get_align_string()}"
            + ")"
        )


class InputField(Widget):
    """A Label that lets you display input"""

    styles: dict[str, StyleType] = {
        "value": default_foreground,
        "cursor": MarkupFormatter("[inverse]{item}"),
        "highlight": Widget.OVERRIDE,
    }

    serialized = Widget.serialized + [
        "value",
        "prompt",
        "cursor",
        "tab_length",
    ]

    def __init__(
        self, value: str = "", prompt: str = "", tab_length: int = 4, padding: int = 0
    ) -> None:
        """Initialize object"""

        super().__init__()
        self._selected_range: tuple[Optional[int], Optional[int]] = (None, None)
        self.prompt = prompt
        self.padding = padding
        self.value = value + " "
        self.tab_length = tab_length
        self.cursor = real_length(value)
        self.width = 40

        self._donor_label = Label(align=Label.ALIGN_LEFT, padding=padding)
        self._donor_label.width = self.width
        self._donor_label.set_style("value", self.get_style("value").method)

    @property
    def selected_value(self) -> Optional[str]:
        """Get text that is selected"""

        start, end = self._selected_range
        if any(value is None for value in [start, end]):
            return None

        return self.value[start:end]

    @property
    def cursor(self) -> int:
        """Return cursor of self"""

        return self._cursor

    @cursor.setter
    def cursor(self, value: int) -> None:
        """Set cursor"""

        self._cursor = min(max(0, value), real_length(self.value) - 1)

    def get_value(self, strip: bool = True) -> str:
        """Get stripped value of object"""

        value = strip_ansi(self.value)
        if strip:
            return value.strip()

        return value

    def clear_value(self) -> str:
        """Reset value of field, return old value"""

        old = strip_ansi(self.value).strip()
        self.value = " "
        self.cursor = 1

        return old

    def clear_selected(self) -> None:
        """Reset self._selected"""

        self._selected_range = (None, None)

    def has_selection(self) -> bool:
        """Return if there is text selected"""

        return all(val is not None for val in self._selected_range)

    def get_lines(self) -> list[str]:
        """Return broken-up lines from object"""

        def _get_label_lines(buff: str) -> list[str]:
            """Get lines from donor label"""

            label = self._donor_label
            label.value = buff
            return label.get_lines()

        def _normalize_cursor(
            coords: tuple[Optional[int], Optional[int]]
        ) -> tuple[int, int]:
            """Figure out switching None positions and ordering"""

            start, end = coords
            if start is None or end is None:
                start = end = self.cursor

            elif start > end:
                start, end = end, start

            return start, end

        self._donor_label.width = self.width
        self._donor_label.padding = self.padding

        lines = []
        buff = ""
        value_style = self.get_style("value")
        cursor_style = self.get_style("cursor")
        highlight_style = self.get_style("highlight")

        # highlight_style is optional
        if highlight_style.method is Widget.OVERRIDE:
            highlight_style = cursor_style

        start, end = _normalize_cursor(self._selected_range)
        self.cursor = end

        for i, char in enumerate(self.prompt + self.value):
            charindex = i - real_length(self.prompt)

            if char == keys.RETURN:
                buff_list = list(buff)
                buff_end = ""

                if self._is_focused and charindex == self.cursor:
                    buff_end = cursor_style(" ")

                lines += _get_label_lines("".join(buff_list) + buff_end)
                buff = ""
                continue

            # currently all lines visually have an extra " " at the end
            if real_length(buff) > self.width:
                lines += _get_label_lines(buff[:-1])

                if char == keys.RETURN:
                    char = " "

                buff = ""

            elif self._is_focused and charindex == self.cursor:
                buff += cursor_style(char)

            elif self._is_focused and start <= charindex <= end:
                buff += highlight_style(char)

            else:
                buff += value_style(char)

        if len(buff) > 0:
            lines += _get_label_lines(buff)

        self.height = len(lines)

        return lines

    def select_range(self, rng: tuple[int, int]) -> None:
        """Overwrite select method to do a visual selection in range"""

        self._selected_range = rng

    def send(self, key: Optional[str]) -> None:
        """Send key to InputField"""

        def _find_newline(step: int) -> int:
            """Find newline in self.value stepping by `step`"""

            if step == -1:
                value = self.value[self.cursor :: step]
            else:
                value = self.value[self.cursor :: step]

            i = 0
            for i, char in enumerate(value):
                if char is keys.RETURN:
                    return i

            return i

        def _find_cursor_line() -> str:
            """Find line that cursor is in"""

            visited = 0
            for line in self.get_value().splitlines():
                new = real_length(line)
                visited += new + 1
                if visited - (1 if new > 0 else 0) >= self.cursor:
                    return line

            return ""

        valid_platform_keys = [
            keys.SPACE,
            keys.CTRL_J,
            keys.CTRL_I,
        ]

        if key is None:
            return

        if key == keys.BACKSPACE:
            if self.cursor <= 0:
                return

            left = self.value[: self.cursor - 1]
            right = self.value[self.cursor :]

            self.value = left + right
            self.send(keys.LEFT)

        elif key is keys.CTRL_I:
            for _ in range(self.tab_length):
                self.send(keys.SPACE)

        elif key in [keys.LEFT, keys.CTRL_B]:
            self.cursor -= 1

        elif key in [keys.RIGHT, keys.CTRL_F]:
            self.cursor += 1

        elif key in [keys.DOWN, keys.CTRL_N]:
            self.cursor += _find_newline(1) + 1

        elif key in [keys.UP, keys.CTRL_P]:
            self.cursor -= max(_find_newline(-1), 1)
            line = _find_cursor_line()
            self.cursor -= real_length(line)

        # `keys.values()` might need to be renamed to something more like
        # `keys.escapes.values()`
        elif key in valid_platform_keys or (
            real_length(key) == 1 and not key in keys.values()
        ):
            left = self.value[: self.cursor]
            right = self.value[self.cursor :]

            self.value = left + key + right
            self.cursor += 1

    def debug(self) -> str:
        """Return identifiable information about object"""

        value = self.value if real_length(self.value) < 7 else "..."

        return (
            "InputField("
            + f'prompt="{self.prompt}", '
            + f'value="{value}", '
            + f"tab_length={self.tab_length}"
            + ")"
        )


class O_Splitter(Widget):
    """A widget that holds sub-widgets, and aligns them next to eachother"""

    chars: dict[str, CharType] = {
        "separator": " | ",
    }

    styles: dict[str, StyleType] = {
        "separator": apply_markup,
    }

    serialized = Widget.serialized + ["arrangement"]

    def __init__(self, arrangement: Optional[str] = None) -> None:
        """Initiate object"""

        super().__init__()
        self.arrangement = arrangement
        self._widgets: list[Widget] = []

    def __add__(self, other: object) -> Splitter:
        """Overload + operator"""

        return self.__iadd__(other)

    def __iadd__(self, other: object) -> Splitter:
        """Overload += operator"""

        if not isinstance(other, Widget):
            raise NotImplementedError("You can only add widgets to a Splitter.")

        self._add_widget(other)
        return self

    def __iter__(self) -> Iterator[Widget]:
        """Iterate through self._widgets"""

        for widget in self._widgets:
            yield widget

    def __getitem__(self, sli: Union[int, slice]) -> Union[Widget, list[Widget]]:
        """Index in self._widget"""

        return self._widgets[sli]

    def __setitem__(self, index: int, value: Any) -> None:
        """Set item in self._widgets"""

        self._widgets[index] = value

    def _add_widget(self, other: Widget) -> None:
        """Add an widget"""

        if other.forced_height is not None:
            other.height = other.forced_height

        if self.height is None:
            self.height += other.height

        self._widgets.append(other)

    def serialize(self) -> dict[str, Any]:
        """Serialize object"""

        out = super().serialize()
        out["_widgets"] = []

        for widget in self._widgets:
            out["_widgets"].append(widget.serialize())

        return out

    def get_lines(self) -> list[str]:
        """Get lines by joining all widgets

        This is not ideal. ListView-s don't work properly, and this object's
        width is not set correctly."""

        widgets = self._widgets

        if len(widgets) == 0:
            return []

        separator_style = self.get_style("separator")
        char = self.get_char("separator")
        assert isinstance(char, str), char
        separator = separator_style(char)

        if self.arrangement is None:
            widget_width = self.width // len(widgets)
            widget_width -= real_length((len(widgets) - 1) * separator)
            widths = [widget_width] * len(widgets)

        else:
            # there should be "fluid" widths, not just static ones.
            widths = [int(val) for val in self.arrangement.split(";")]

        for i, widget in enumerate(widgets):
            if widget.forced_width is None:
                try:
                    widget.width = widths[i]
                except IndexError as error:
                    raise ValueError(
                        "There were not enough widths supplied in the arrangement:"
                        + f" expected {len(widgets)}, got {len(widths)}."
                    ) from error

        lines = []
        widget_lines = [widget.get_lines() for widget in widgets]

        for horizontal in zip(*widget_lines):
            lines.append(separator.join(horizontal))

        self.width = max(real_length(line) for line in lines) - 1

        if self.forced_height is None:
            self.height = len(lines)

        return lines

    def debug(self) -> str:
        """Debug identifiable information about objects"""

        out = "Splitter(), widgets=["
        for widget in self._widgets:
            out += type(widget).__name__ + ", "

        out = out.strip(", ")
        out += "]"

        return out
