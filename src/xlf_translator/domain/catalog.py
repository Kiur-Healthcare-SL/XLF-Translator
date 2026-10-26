from collections import Counter
from collections.abc import Callable, Iterable

from xlf_translator.domain.catalog_refusal import CatalogRefusal
from xlf_translator.domain.translation_unit import TranslationUnit
from xlf_translator.domain.unit_identifier import UnitIdentifier

UnitPredicate = Callable[[TranslationUnit], bool]


class Catalog:
    """The translation units of a document, in document order, addressed by ordinal from 1."""

    def __init__(self, units: Iterable[TranslationUnit]):
        self._units = tuple(units)

    @staticmethod
    def of(units: Iterable[TranslationUnit]) -> "Catalog | CatalogRefusal":
        catalog = Catalog(units)
        duplicated = catalog._duplicated()
        if duplicated:
            return CatalogRefusal("unique trans-unit identifiers", f"'{duplicated[0]}' more than once")
        return catalog

    def _duplicated(self) -> list[UnitIdentifier]:
        tally = Counter()
        for unit in self._units:
            unit.tally_into(tally)
        return [identifier for identifier, count in tally.items() if count > 1]

    def size(self) -> int:
        return len(self._units)

    def contains(self, ordinal: int) -> bool:
        return 1 <= ordinal <= self.size()

    def unit_at(self, ordinal: int) -> TranslationUnit:
        return self._units[ordinal - 1]

    def ordinals_where(self, predicate: UnitPredicate) -> tuple[int, ...]:
        return tuple(ordinal for ordinal, unit in enumerate(self._units, start=1) if predicate(unit))

    def every(self, predicate: UnitPredicate) -> bool:
        return all(predicate(unit) for unit in self._units)

    def with_unit(self, ordinal: int, unit: TranslationUnit) -> "Catalog":
        return Catalog(self._units[: ordinal - 1] + (unit,) + self._units[ordinal:])

    def with_target(self, identifier: UnitIdentifier, masked: str) -> "Catalog":
        return Catalog(self._retargeted(unit, identifier, masked) for unit in self._units)

    @staticmethod
    def _retargeted(unit: TranslationUnit, identifier: UnitIdentifier, masked: str) -> TranslationUnit:
        return unit.with_target(masked) if unit.is_identified_by(identifier) else unit

    def write_into(self, sink) -> None:
        for unit in self._units:
            unit.write_into(sink)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Catalog) and self._units == other._units

    def __hash__(self) -> int:
        return hash(self._units)
