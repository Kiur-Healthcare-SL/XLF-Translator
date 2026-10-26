from support.content_samples import BOLD_PHRASE
from support.recorders import described

from xlf_translator.domain.content import Content
from xlf_translator.domain.translation import Translation
from xlf_translator.domain.unit_state import UnitState


def fresh(source=BOLD_PHRASE):
    return Translation.parsed(source, None)


def test_states_follow_the_target():
    assert fresh().state() is UnitState.UNTRANSLATED
    assert fresh().with_target("{1}done{2}").state() is UnitState.TRANSLATED
    assert fresh().with_target("{1}done").state() is UnitState.INVALID


def test_a_blank_source_is_auto_filled_and_restored():
    blank = fresh(Content.of_text("  "))
    assert blank.is_auto_filled()
    assert blank.state() is UnitState.TRANSLATED
    assert blank.with_target("").state() is UnitState.TRANSLATED
    assert blank.with_target("") == blank


def test_a_parsed_target_is_masked_against_its_source():
    assert Translation.parsed(BOLD_PHRASE, BOLD_PHRASE) == fresh().with_source_copied()


def test_an_untranslated_target_has_no_unmasked_form():
    assert fresh().unmasked_target() is None
    assert fresh().with_source_copied().unmasked_target() == BOLD_PHRASE


def test_a_translation_describes_itself():
    description = described(fresh().with_target("{1}x"))
    assert description["texts"] == ("{1}limited functionality{2}", "{1}x")
    assert description["state"] == ("invalid", False, ("{2} (</b>) is missing",))


def test_an_auto_filled_target_unmasks_to_its_source():
    blank = Content.of_text("   ")
    assert fresh(blank).unmasked_target() == blank
