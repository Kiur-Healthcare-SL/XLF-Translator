from xlf_translator.domain.content import Content
from xlf_translator.domain.placeholder_comparison import PlaceholderComparison
from xlf_translator.domain.source_content import SourceContent
from xlf_translator.domain.target_content import TargetContent
from xlf_translator.domain.unit_state import UnitState


class Translation:
    """A source and its target, and the state they put a unit in (design D13).

    A whitespace-only source needs no translation: its target is the source,
    and clearing that target restores it.
    """

    def __init__(self, source: SourceContent, target: TargetContent):
        self._source = source
        self._target = target
        if source.is_blank() and target.is_blank():
            self._target = TargetContent(source.masked())

    @staticmethod
    def parsed(source: Content, target: Content | None) -> "Translation":
        masked = SourceContent(source).mask(target or Content([]))
        return Translation(SourceContent(source), TargetContent(masked))

    def state(self) -> UnitState:
        if self._source.is_blank():
            return UnitState.TRANSLATED
        if self._target.is_blank():
            return UnitState.UNTRANSLATED
        return UnitState.TRANSLATED if self.difference().matches() else UnitState.INVALID

    def is_auto_filled(self) -> bool:
        return self._source.is_blank()

    def difference(self) -> PlaceholderComparison:
        return self._target.compared_with(self._source)

    def with_target(self, masked: str) -> "Translation":
        return Translation(self._source, TargetContent(masked))

    def with_source_copied(self) -> "Translation":
        return self.with_target(self._source.masked())

    def unmasked_target(self) -> Content | None:
        return None if self.state() is UnitState.UNTRANSLATED else self._target.unmasked_by(self._source)

    def describe_into(self, builder) -> None:
        builder.texts(self._source.masked(), str(self._target))
        builder.state(self.state().value, self.is_auto_filled(), self.difference().problems())

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Translation) and (self._source, self._target) == (other._source, other._target)

    def __hash__(self) -> int:
        return hash((self._source, self._target))

    def __repr__(self) -> str:
        return f"Translation({self._source!r}, {self._target!r})"
