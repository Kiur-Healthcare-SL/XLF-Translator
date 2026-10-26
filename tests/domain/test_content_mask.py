from support.content_samples import BOLD_PHRASE, CLOSE_BOLD, OPEN_BOLD, content

from xlf_translator.domain.content import Content
from xlf_translator.domain.content_mask import ContentMask


def masked(source, target=None):
    return ContentMask(source).mask(target or source)


def test_a_paired_placeholder_becomes_two_tokens():
    assert masked(BOLD_PHRASE) == "{1}limited functionality{2}"


def test_text_without_placeholders_is_unchanged():
    text = "  Volver al listado "
    assert masked(Content.of_text(text)) == text


def test_escaped_markup_is_not_a_placeholder():
    assert masked(Content.of_text("<p><b>Tip</b></p>")) == "<p><b>Tip</b></p>"


def test_literal_braces_are_doubled():
    assert masked(Content.of_text("Patrón: {serie}_{1}.dcm")) == "Patrón: {{serie}}_{{1}}.dcm"


def test_a_target_is_numbered_against_its_source():
    target = content(CLOSE_BOLD, "word", OPEN_BOLD)
    assert masked(BOLD_PHRASE, target) == "{2}word{1}"


def test_repeated_placeholders_take_source_occurrences_in_turn():
    source = content(OPEN_BOLD, "a", CLOSE_BOLD, OPEN_BOLD, "b", CLOSE_BOLD)
    assert masked(source) == "{1}a{2}{3}b{4}"


def test_a_placeholder_the_source_lacks_is_numbered_past_the_source():
    target = content(OPEN_BOLD, "x", OPEN_BOLD)
    assert masked(content(OPEN_BOLD, "x"), target) == "{1}x{2}"
