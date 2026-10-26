from support.catalog_samples import AUTO_FILLED, INVALID, TRANSLATED, UNTRANSLATED, catalog

from xlf_translator.domain.catalog_classification import CatalogClassification


def test_a_catalog_of_untranslated_units_is_fresh():
    assert CatalogClassification.of(catalog(UNTRANSLATED, UNTRANSLATED)) is CatalogClassification.FRESH


def test_an_auto_filled_unit_keeps_a_catalog_fresh():
    assert CatalogClassification.of(catalog(UNTRANSLATED, AUTO_FILLED)) is CatalogClassification.FRESH


def test_a_gap_makes_a_catalog_partial():
    assert CatalogClassification.of(catalog(TRANSLATED, UNTRANSLATED)) is CatalogClassification.PARTIAL


def test_imported_damage_makes_a_catalog_partial():
    assert CatalogClassification.of(catalog(TRANSLATED, INVALID)) is CatalogClassification.PARTIAL


def test_a_fully_translated_catalog_is_completed():
    assert CatalogClassification.of(catalog(TRANSLATED, AUTO_FILLED)) is CatalogClassification.COMPLETED
