from collections.abc import Iterable, Iterator
from itertools import groupby

from xlf_translator.domain.placeholder import Placeholder
from xlf_translator.domain.text_run import TextRun


class Content:
    """The content of a source or target: text runs and placeholders, in order."""

    def __init__(self, items: Iterable[TextRun | Placeholder]):
        self._items = Content._normalised(items)

    @staticmethod
    def of_text(text: str) -> "Content":
        return Content([TextRun(text)])

    @staticmethod
    def _normalised(items: Iterable[TextRun | Placeholder]) -> tuple[TextRun | Placeholder, ...]:
        groups = groupby(items, key=type)
        return tuple(item for kind, group in groups for item in kind.combined(list(group)))

    def placeholders(self) -> tuple[Placeholder, ...]:
        return tuple(placeholder for item in self._items for placeholder in item.placeholders())

    def is_blank(self) -> bool:
        return all(item.is_blank() for item in self._items)

    def write_into(self, sink) -> None:
        for item in self._items:
            item.write_into(sink)

    def __iter__(self) -> Iterator[TextRun | Placeholder]:
        return iter(self._items)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Content) and self._items == other._items

    def __hash__(self) -> int:
        return hash(self._items)

    def __repr__(self) -> str:
        return f"Content({list(self._items)!r})"
