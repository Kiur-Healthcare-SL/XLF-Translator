from collections import Counter

from xlf_translator.domain.content import Content
from xlf_translator.domain.placeholder_comparison import PlaceholderComparison
from xlf_translator.domain.translation import Translation
from xlf_translator.domain.unit_identifier import UnitIdentifier
from xlf_translator.domain.unit_state import UnitState


class TranslationUnit:
    """One trans-unit: its identifier and its translation."""

    def __init__(self, identifier: UnitIdentifier, translation: Translation):
        self._identifier = identifier
        self._translation = translation

    @staticmethod
    def parsed(identifier: UnitIdentifier, source: Content, target: Content | None) -> "TranslationUnit":
        return TranslationUnit(identifier, Translation.parsed(source, target))

    def is_translated(self) -> bool:
        return self._translation.state() is UnitState.TRANSLATED

    def is_untranslated(self) -> bool:
        return self._translation.state() is UnitState.UNTRANSLATED

    def is_invalid(self) -> bool:
        return self._translation.state() is UnitState.INVALID

    def is_unresolved(self) -> bool:
        return not self.is_translated()

    def is_auto_filled(self) -> bool:
        return self._translation.is_auto_filled()

    def is_identified_by(self, identifier: UnitIdentifier) -> bool:
        return self._identifier == identifier

    def difference(self) -> PlaceholderComparison:
        return self._translation.difference()

    def with_target(self, masked: str) -> "TranslationUnit":
        return TranslationUnit(self._identifier, self._translation.with_target(masked))

    def with_source_copied(self) -> "TranslationUnit":
        return TranslationUnit(self._identifier, self._translation.with_source_copied())

    def describe_into(self, builder) -> None:
        builder.identifier(str(self._identifier))
        self._translation.describe_into(builder)

    def write_into(self, sink) -> None:
        sink.unit(str(self._identifier), self._translation.unmasked_target(), self)

    def tally_into(self, tally: Counter) -> None:
        tally[self._identifier] += 1

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TranslationUnit) and (self._identifier, self._translation) == (
            other._identifier,
            other._translation,
        )

    def __hash__(self) -> int:
        return hash((self._identifier, self._translation))

    def __repr__(self) -> str:
        return f"TranslationUnit({self._identifier!r}, {self._translation!r})"
