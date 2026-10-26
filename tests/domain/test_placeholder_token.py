import pytest

from xlf_translator.domain.placeholder_token import PlaceholderToken


def test_a_token_renders_in_braces():
    assert str(PlaceholderToken(1)) == "{1}"


def test_a_multi_digit_token_parses():
    assert PlaceholderToken.parse("{10}") == PlaceholderToken(10)


@pytest.mark.parametrize("text", ["{0}", "{1", "1}", "{01}", "{a}", "{{1}}", ""])
def test_malformed_tokens_do_not_parse(text):
    assert PlaceholderToken.parse(text) is None


def test_token_zero_cannot_be_built():
    with pytest.raises(ValueError):
        PlaceholderToken(0)


def test_a_token_selects_the_placeholder_it_numbers():
    assert PlaceholderToken(2).select_from(("first", "second")) == "second"
    assert PlaceholderToken(3).select_from(("first", "second")) is None


def test_tokens_order_by_number():
    assert sorted([PlaceholderToken(10), PlaceholderToken(2)]) == [PlaceholderToken(2), PlaceholderToken(10)]
