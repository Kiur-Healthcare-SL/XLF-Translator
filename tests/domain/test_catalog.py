from support.catalog_samples import AUTO_FILLED, TRANSLATED, UNTRANSLATED, catalog, unit
from support.recorders import DescriptionRecorder

from xlf_translator.domain.catalog import Catalog
from xlf_translator.domain.catalog_refusal import CatalogRefusal
from xlf_translator.domain.unit_identifier import UnitIdentifier


def test_units_keep_document_order_and_are_found_by_ordinal():
    sample = catalog(TRANSLATED, UNTRANSLATED, AUTO_FILLED)
    assert sample.size() == 3
    assert sample.unit_at(2) == unit(2, UNTRANSLATED)
    assert sample.ordinals_where(lambda each: each.is_untranslated()) == (2,)


def test_ordinals_outside_the_catalog_are_not_contained():
    sample = catalog(TRANSLATED, TRANSLATED)
    assert [sample.contains(ordinal) for ordinal in (0, 1, 2, 3)] == [False, True, True, False]


def test_duplicate_identifiers_are_refused():
    refused = Catalog.of([unit(1, TRANSLATED), unit(1, UNTRANSLATED)])
    assert refused == CatalogRefusal("unique trans-unit identifiers", "'unit.1' more than once")


def test_unique_identifiers_make_a_catalog():
    assert isinstance(Catalog.of([unit(1, TRANSLATED), unit(2, TRANSLATED)]), Catalog)


def test_a_target_is_entered_by_identifier():
    sample = catalog(UNTRANSLATED, UNTRANSLATED)
    entered = sample.with_target(UnitIdentifier("unit.2"), "{1}done{2}")
    assert entered.ordinals_where(lambda each: each.is_translated()) == (2,)


def test_a_unit_is_replaced_by_ordinal():
    assert catalog(UNTRANSLATED, UNTRANSLATED).with_unit(1, unit(1, TRANSLATED)) == catalog(TRANSLATED, UNTRANSLATED)


def test_a_catalog_writes_every_unit_in_order():
    written = []

    class Sink(DescriptionRecorder):
        def unit(self, identifier, target, unit):
            written.append(identifier)

    catalog(TRANSLATED, UNTRANSLATED).write_into(Sink())
    assert written == ["unit.1", "unit.2"]
