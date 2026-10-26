from collections import Counter

from support.content_samples import BOLD_PHRASE
from support.recorders import described

from xlf_translator.domain.content import Content
from xlf_translator.domain.translation_unit import TranslationUnit
from xlf_translator.domain.unit_identifier import UnitIdentifier

IDENTIFIER = UnitIdentifier("viewer.limitedMode")


def parsed(source=BOLD_PHRASE, target=None):
    return TranslationUnit.parsed(IDENTIFIER, source, target)


def test_an_empty_target_is_untranslated():
    assert parsed().is_untranslated()


def test_a_whitespace_only_target_is_untranslated():
    assert parsed(Content.of_text("Hallazgos")).with_target("   ").is_untranslated()


def test_a_target_matching_its_source_placeholders_is_translated():
    assert parsed().with_target("{2}word{1}").is_translated()


def test_a_target_missing_a_placeholder_is_invalid():
    unit = parsed().with_target("{1}word")
    assert unit.is_invalid()
    assert unit.is_unresolved()


def test_a_target_equal_to_its_source_is_translated():
    assert parsed(target=BOLD_PHRASE).is_translated()


def test_a_whitespace_only_source_is_auto_filled_and_translated():
    unit = parsed(Content.of_text("   "))
    assert unit.is_auto_filled()
    assert unit.is_translated()


def test_clearing_an_auto_filled_target_restores_the_source():
    unit = parsed(Content.of_text("   "))
    cleared = unit.with_target("")
    assert cleared == unit
    assert described(cleared)["texts"] == ("   ", "   ")


def test_copying_the_source_translates_the_unit():
    assert parsed().with_source_copied().is_translated()


def test_a_unit_knows_its_identifier():
    assert parsed().is_identified_by(IDENTIFIER)
    tally = Counter()
    parsed().tally_into(tally)
    assert tally == Counter({IDENTIFIER: 1})


def test_a_unit_writes_its_identifier_and_unmasked_target():
    translated = parsed(target=BOLD_PHRASE)
    assert described(translated, "write_into")["unit"] == ("viewer.limitedMode", BOLD_PHRASE, translated)
    assert described(parsed(), "write_into")["unit"] == ("viewer.limitedMode", None, parsed())


def test_a_unit_describes_its_auto_filled_mark():
    assert described(parsed(Content.of_text(" ")))["state"] == ("translated", True, ())
