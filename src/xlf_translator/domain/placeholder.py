from collections.abc import Iterator

from xlf_translator.domain.placeholder_attributes import PlaceholderAttributes
from xlf_translator.domain.placeholder_name import PlaceholderName
from xlf_translator.domain.placeholder_token import PlaceholderToken


class Placeholder:
    """An inline `<x/>` element: its name and every attribute, in order."""

    def __init__(self, name: PlaceholderName, attributes: PlaceholderAttributes):
        self._name = name
        self._attributes = attributes

    @staticmethod
    def combined(placeholders: list["Placeholder"]) -> list["Placeholder"]:
        return placeholders

    def markup(self) -> str:
        return self._attributes.equivalent_text() or f'<x id="{self._name}"/>'

    def masked(self, numbers: Iterator[int]) -> str:
        return str(PlaceholderToken(next(numbers)))

    def placeholders(self) -> tuple["Placeholder", ...]:
        return (self,)

    def is_blank(self) -> bool:
        return False

    def write_into(self, sink) -> None:
        sink.placeholder(tuple(self._attributes))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Placeholder) and (self._name, self._attributes) == (other._name, other._attributes)

    def __hash__(self) -> int:
        return hash((self._name, self._attributes))

    def __repr__(self) -> str:
        return f"Placeholder({self._name!r})"
