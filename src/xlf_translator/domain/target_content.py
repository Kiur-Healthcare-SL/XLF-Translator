from xlf_translator.domain.content import Content
from xlf_translator.domain.placeholder_comparison import PlaceholderComparison
from xlf_translator.domain.source_content import SourceContent


class TargetContent:
    """A target as the translator edits it: text with `{n}` tokens."""

    def __init__(self, masked: str):
        self._masked = masked

    def is_blank(self) -> bool:
        return self._masked.strip() == ""

    def compared_with(self, source: SourceContent) -> PlaceholderComparison:
        return source.compare(self._masked)

    def unmasked_by(self, source: SourceContent) -> Content:
        return source.unmask(self._masked)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TargetContent) and self._masked == other._masked

    def __hash__(self) -> int:
        return hash(self._masked)

    def __str__(self) -> str:
        return self._masked

    def __repr__(self) -> str:
        return f"TargetContent({self._masked!r})"
