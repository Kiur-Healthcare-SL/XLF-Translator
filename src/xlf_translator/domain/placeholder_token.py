import re

TOKEN_SHAPE = re.compile(r"\{([1-9][0-9]*)\}")


class PlaceholderToken:
    """The `{n}` a translator sees in place of the n-th placeholder of a source."""

    def __init__(self, number: int):
        if number < 1:
            raise ValueError(f"Placeholder tokens count from 1, not {number}")
        self._number = number

    @staticmethod
    def parse(text: str) -> "PlaceholderToken | None":
        match = TOKEN_SHAPE.fullmatch(text)
        return match and PlaceholderToken(int(match.group(1)))

    def select_from(self, placeholders: tuple) -> object | None:
        return placeholders[self._number - 1] if self._number <= len(placeholders) else None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PlaceholderToken) and self._number == other._number

    def __lt__(self, other: "PlaceholderToken") -> bool:
        return self._number < other._number

    def __hash__(self) -> int:
        return hash(self._number)

    def __str__(self) -> str:
        return f"{{{self._number}}}"

    def __repr__(self) -> str:
        return f"PlaceholderToken({self._number})"
