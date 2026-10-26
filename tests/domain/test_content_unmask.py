from support.content_samples import BOLD_PHRASE, CLOSE_BOLD, OPEN_BOLD, content

from xlf_translator.domain.content import Content
from xlf_translator.domain.content_mask import ContentMask
from xlf_translator.domain.content_unmask import ContentUnmask


def unmasked(source, masked):
    return ContentUnmask(source).unmask(masked)


def test_tokens_restore_placeholders_in_order():
    assert unmasked(BOLD_PHRASE, "{1}limited functionality{2}") == BOLD_PHRASE


def test_reversed_tokens_restore_in_reversed_order():
    assert unmasked(BOLD_PHRASE, "{2}word{1}") == content(CLOSE_BOLD, "word", OPEN_BOLD)


def test_placeholder_attributes_survive_a_round_trip():
    restored = unmasked(BOLD_PHRASE, ContentMask(BOLD_PHRASE).mask(BOLD_PHRASE))
    assert restored.placeholders() == (OPEN_BOLD, CLOSE_BOLD)


def test_literal_braces_round_trip_and_yield_no_token():
    source = Content.of_text("Patrón: {serie}_{1}.dcm")
    masked = ContentMask(source).mask(source)
    restored = unmasked(source, masked)
    assert restored == source
    assert restored.placeholders() == ()


def test_unknown_tokens_and_lone_braces_stay_literal():
    assert unmasked(BOLD_PHRASE, "{9} a { b }") == Content.of_text("{9} a { b }")
