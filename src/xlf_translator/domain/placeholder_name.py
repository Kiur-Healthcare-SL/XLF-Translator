class PlaceholderName:
    """The id of an inline `<x/>` placeholder, such as `START_BOLD_TEXT`."""

    def __init__(self, value: str):
        self._value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PlaceholderName) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"PlaceholderName({self._value!r})"
