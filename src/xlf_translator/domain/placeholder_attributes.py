from collections.abc import Iterator

EQUIVALENT_TEXT = "equiv-text"


class PlaceholderAttributes:
    """Every attribute of an inline `<x/>` placeholder, in document order."""

    def __init__(self, pairs: tuple[tuple[str, str], ...]):
        self._pairs = tuple(pairs)

    def equivalent_text(self) -> str | None:
        return dict(self._pairs).get(EQUIVALENT_TEXT)

    def __iter__(self) -> Iterator[tuple[str, str]]:
        return iter(self._pairs)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PlaceholderAttributes) and self._pairs == other._pairs

    def __hash__(self) -> int:
        return hash(self._pairs)

    def __repr__(self) -> str:
        return f"PlaceholderAttributes({self._pairs!r})"
