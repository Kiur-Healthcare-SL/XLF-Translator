from enum import Enum

from xlf_translator.domain.catalog import Catalog


class CatalogClassification(Enum):
    """What an upload is, judged only by its content."""

    FRESH = "fresh"
    PARTIAL = "partial"
    COMPLETED = "completed"

    @staticmethod
    def of(catalog: Catalog) -> "CatalogClassification":
        if catalog.every(lambda unit: unit.is_translated()):
            return CatalogClassification.COMPLETED
        if catalog.every(lambda unit: unit.is_auto_filled() or unit.is_untranslated()):
            return CatalogClassification.FRESH
        return CatalogClassification.PARTIAL
