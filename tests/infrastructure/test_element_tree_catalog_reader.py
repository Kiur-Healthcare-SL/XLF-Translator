import pytest
from support.fixture_documents import COMPLETED, FRESH, PARTIAL, document, read, trans_unit, xliff
from support.recorders import described

from xlf_translator.domain.catalog_refusal import CatalogRefusal
from xlf_translator.domain.completion_report import CompletionReport
from xlf_translator.domain.language_code import LanguageCode
from xlf_translator.domain.language_pair import LanguagePair
from xlf_translator.infrastructure.element_tree_catalog_reader import ElementTreeCatalogReader


def texts(catalog, ordinal):
    return described(catalog.unit_at(ordinal))["texts"]


def refusal_for(text):
    refusal = ElementTreeCatalogReader().read(document(text))
    assert isinstance(refusal, CatalogRefusal)
    return str(refusal)


def test_the_fresh_fixture_parses_to_sixty_units_in_order():
    catalog, languages = read(FRESH)
    assert catalog.size() == 60
    assert described(catalog.unit_at(1))["identifier"] == "app.title"
    assert described(catalog.unit_at(60))["identifier"] == "about.version"
    assert languages == LanguagePair(LanguageCode("es"))


def test_whitespace_and_inline_placeholders_are_intact():
    catalog, _ = read(FRESH)
    assert texts(catalog, 8)[0] == "  Volver al listado"
    assert texts(catalog, 5)[0] == "Modo de {1}funcionalidad limitada{2} activo"
    assert texts(catalog, 23)[0].count("{") == 10
    assert texts(catalog, 36)[0].startswith("<p><b>Consejo</b></p>")


def test_the_partial_fixture_yields_targets_and_its_target_language():
    catalog, languages = read(PARTIAL)
    imported = catalog.ordinals_where(lambda unit: described(unit)["texts"][1] != "" and not unit.is_auto_filled())
    assert len(imported) == 58
    assert languages == LanguagePair(LanguageCode("es"), LanguageCode("en-GB"))
    assert CompletionReport(catalog).unresolved() == (31, 38, 44, 52)


def test_the_completed_fixture_is_complete():
    catalog, _ = read(COMPLETED)
    assert CompletionReport(catalog).is_complete()


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("not xml at all", "well-formed XML"),
        ("<xliff", "well-formed XML"),
        ('<?xml version="1.0" encoding="ISO-8859-1"?><xliff/>', "encoding ISO-8859-1"),
        (xliff(trans_unit("a", "x"), version="2.0"), "found version 2.0"),
        ('<xliff version="1.2" xmlns="urn:oasis:names:tc:xliff:document:1.2"/>', "<file>"),
        (xliff(trans_unit("a", "x"), file_attributes='target-language="fr"'), "a source language"),
        (xliff(""), "at least one trans-unit"),
        (xliff(trans_unit("a", "x") + "\n" + trans_unit("a", "y")), "'a' more than once"),
        (xliff(trans_unit("a", "x<g id='1'>y</g>")), "<g> in trans-unit 'a'"),
        (xliff(trans_unit("", "x")), "an id and a <source>"),
        ("<html/>", "<xliff> root element"),
    ],
)
def test_untranslatable_documents_are_refused_with_a_reason(text, expected):
    reason = refusal_for(text)
    assert reason.startswith("Expected ")
    assert expected in reason


def test_invalid_utf_8_bytes_are_refused():
    assert "UTF-8" in refusal_for(xliff(trans_unit("a", "x")).encode("utf-8").replace(b"x", b"\xff"))


def test_wrong_version_names_both_versions():
    reason = refusal_for(xliff(trans_unit("a", "x"), version="2.0"))
    assert "1.2" in reason
    assert "2.0" in reason
