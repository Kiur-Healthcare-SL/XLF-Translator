from xlf_translator.domain.content import Content
from xlf_translator.domain.placeholder import Placeholder


class ContentMask:
    """Masks content as text with `{n}` tokens, numbering against a source.

    Each placeholder takes the number of the source placeholder it equals; a
    repeated placeholder takes its source occurrences in turn, and one the
    source lacks is numbered past the source's last token. Literal braces are
    doubled so they cannot be read as tokens.
    """

    def __init__(self, source: Content):
        self._reference = source.placeholders()

    def mask(self, content: Content) -> str:
        numbers = iter(self._numbers(content.placeholders()))
        return "".join(item.masked(numbers) for item in content)

    def _numbers(self, placeholders: tuple[Placeholder, ...]) -> list[int]:
        known = [self._known_number(placeholders, position) for position in range(len(placeholders))]
        unknown = iter(range(len(self._reference) + 1, len(self._reference) + len(placeholders) + 1))
        return [number or next(unknown) for number in known]

    def _known_number(self, placeholders: tuple[Placeholder, ...], position: int) -> int | None:
        placeholder = placeholders[position]
        occurrence = placeholders[:position].count(placeholder)
        matches = [number for number, candidate in enumerate(self._reference, start=1) if candidate == placeholder]
        return matches[occurrence] if occurrence < len(matches) else None
