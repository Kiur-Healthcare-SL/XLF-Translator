from support.content_samples import BOLD_PHRASE

from xlf_translator.domain.content import Content
from xlf_translator.domain.placeholder_comparison import PlaceholderComparison


def compared(target, source=BOLD_PHRASE):
    return PlaceholderComparison(source, target)


def test_a_deleted_token_is_named_with_its_markup():
    comparison = compared("{1}limited")
    assert not comparison.matches()
    assert comparison.problems() == ("{2} (</b>) is missing",)


def test_a_repeated_token_is_reported():
    comparison = compared("{1}a{1}b{2}")
    assert comparison.problems() == ("{1} (<b>) is repeated",)


def test_an_unknown_token_is_reported():
    comparison = compared("{1}a{2}{9}")
    assert comparison.problems() == ("{9} is unknown",)


def test_reordered_tokens_match():
    assert compared("{2}word{1}").matches()


def test_escaped_braces_are_not_tokens():
    source = Content.of_text("Patrón: {serie}_{1}.dcm")
    assert compared("Pattern: {{serie}}_{{1}}.dcm", source).matches()


def test_a_literal_token_shaped_text_is_no_token():
    assert compared("{{1}}", Content.of_text("{1}")).matches()
