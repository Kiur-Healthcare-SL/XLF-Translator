from xlf_translator.domain.content import Content
from xlf_translator.domain.content_mask import ContentMask
from xlf_translator.domain.content_unmask import ContentUnmask
from xlf_translator.domain.placeholder_comparison import PlaceholderComparison


class SourceContent:
    """The source of a unit, against which its target is masked, unmasked and compared."""

    def __init__(self, content: Content):
        self._content = content

    def is_blank(self) -> bool:
        return self._content.is_blank()

    def masked(self) -> str:
        return self.mask(self._content)

    def mask(self, target: Content) -> str:
        return ContentMask(self._content).mask(target)

    def unmask(self, masked_target: str) -> Content:
        return ContentUnmask(self._content).unmask(masked_target)

    def compare(self, masked_target: str) -> PlaceholderComparison:
        return PlaceholderComparison(self._content, masked_target)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SourceContent) and self._content == other._content

    def __hash__(self) -> int:
        return hash(self._content)

    def __repr__(self) -> str:
        return f"SourceContent({self._content!r})"
