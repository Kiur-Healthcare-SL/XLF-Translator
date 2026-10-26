from xlf_translator.domain.auto_fill_report import AutoFillReport
from xlf_translator.domain.catalog import Catalog
from xlf_translator.domain.catalog_classification import CatalogClassification
from xlf_translator.domain.completion_report import CompletionReport
from xlf_translator.domain.translation_unit import TranslationUnit
from xlf_translator.domain.unit_identifier import UnitIdentifier


class CatalogPosition:
    """The current unit of a catalog, as an ordinal counted from 1."""

    def __init__(self, catalog: Catalog, ordinal: int):
        self._catalog = catalog
        self._ordinal = ordinal

    @staticmethod
    def resumed(catalog: Catalog) -> "CatalogPosition":
        unresolved = CompletionReport(catalog).unresolved()
        return CatalogPosition(catalog, unresolved[0] if unresolved else 1)

    def forward(self) -> "CatalogPosition":
        return self.jump(self._ordinal + 1)

    def backward(self) -> "CatalogPosition":
        return self.jump(self._ordinal - 1)

    def jump(self, ordinal: int) -> "CatalogPosition":
        return CatalogPosition(self._catalog, ordinal) if self._catalog.contains(ordinal) else self

    def contains(self, ordinal: int) -> bool:
        return self._catalog.contains(ordinal)

    def current(self) -> TranslationUnit:
        return self._catalog.unit_at(self._ordinal)

    def with_target(self, identifier: UnitIdentifier, masked: str) -> "CatalogPosition":
        return CatalogPosition(self._catalog.with_target(identifier, masked), self._ordinal)

    def with_source_copied(self) -> "CatalogPosition":
        copied = self.current().with_source_copied()
        return CatalogPosition(self._catalog.with_unit(self._ordinal, copied), self._ordinal)

    def classification(self) -> CatalogClassification:
        return CatalogClassification.of(self._catalog)

    def completion(self) -> CompletionReport:
        return CompletionReport(self._catalog)

    def auto_fill(self) -> AutoFillReport:
        return AutoFillReport(self._catalog)

    def write_with(self, writer, document, language) -> bytes:
        return writer.write(document, self._catalog, language)

    def describe_into(self, builder) -> None:
        builder.position(self._ordinal, self._catalog.size())

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CatalogPosition) and (self._catalog, self._ordinal) == (other._catalog, other._ordinal)

    def __hash__(self) -> int:
        return hash((self._catalog, self._ordinal))
