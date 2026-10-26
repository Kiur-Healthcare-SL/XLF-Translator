from collections.abc import Iterator

BRACE_ESCAPES = str.maketrans({"{": "{{", "}": "}}"})


class TextRun:
    """Literal characters between placeholders, markup-looking text included."""

    def __init__(self, text: str):
        self._text = text

    @staticmethod
    def combined(runs: list["TextRun"]) -> list["TextRun"]:
        text = "".join(run._text for run in runs)
        return [TextRun(text)] if text else []

    def masked(self, numbers: Iterator[int]) -> str:
        return self._text.translate(BRACE_ESCAPES)

    def placeholders(self) -> tuple:
        return ()

    def is_blank(self) -> bool:
        return self._text.strip() == ""

    def write_into(self, sink) -> None:
        sink.text(self._text)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TextRun) and self._text == other._text

    def __hash__(self) -> int:
        return hash(self._text)

    def __repr__(self) -> str:
        return f"TextRun({self._text!r})"
