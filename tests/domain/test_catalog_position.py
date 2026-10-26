from support.catalog_samples import TRANSLATED, UNTRANSLATED, catalog, catalog_with
from support.recorders import described

from xlf_translator.domain.catalog_position import CatalogPosition
from xlf_translator.domain.unit_identifier import UnitIdentifier

SIXTY = catalog_with(60)


def test_the_position_reports_ordinal_and_total():
    assert described(CatalogPosition(SIXTY, 7))["position"] == (7, 60)


def test_stepping_moves_one_unit():
    assert CatalogPosition(SIXTY, 7).forward() == CatalogPosition(SIXTY, 8)
    assert CatalogPosition(SIXTY, 7).backward() == CatalogPosition(SIXTY, 6)


def test_stepping_past_either_end_is_refused():
    assert CatalogPosition(SIXTY, 60).forward() == CatalogPosition(SIXTY, 60)
    assert CatalogPosition(SIXTY, 1).backward() == CatalogPosition(SIXTY, 1)


def test_jumping_to_an_ordinal():
    assert CatalogPosition(SIXTY, 7).jump(52) == CatalogPosition(SIXTY, 52)
    assert CatalogPosition(SIXTY, 7).jump(500) == CatalogPosition(SIXTY, 7)


def test_resuming_lands_on_the_first_unresolved_unit_or_the_first():
    assert CatalogPosition.resumed(catalog_with(60, untranslated=[31])) == CatalogPosition(
        catalog_with(60, untranslated=[31]), 31
    )
    assert CatalogPosition.resumed(SIXTY) == CatalogPosition(SIXTY, 1)


def test_a_target_is_entered_without_moving():
    position = CatalogPosition(catalog(UNTRANSLATED, UNTRANSLATED), 1)
    entered = position.with_target(UnitIdentifier("unit.2"), "{1}done{2}")
    assert entered == CatalogPosition(catalog(UNTRANSLATED, TRANSLATED), 1)


def test_the_current_source_is_copied_into_its_target():
    position = CatalogPosition(catalog(UNTRANSLATED, UNTRANSLATED), 2)
    assert position.with_source_copied().current().is_translated()


def test_reports_cover_the_whole_catalog():
    position = CatalogPosition(catalog_with(3, untranslated=[2]), 1)
    assert position.completion().unresolved() == (2,)
    assert position.classification().value == "partial"
    assert position.auto_fill().ordinals() == ()
