import pytest

from xlf_translator.domain.language_code import LanguageCode


@pytest.mark.parametrize("value", ["es", "fr", "en-GB", "zh-Hant-TW"])
def test_well_formed_tags_are_accepted(value):
    assert str(LanguageCode(value)) == value


@pytest.mark.parametrize("value", ["", "e", "english", "en_GB", "en-", "-GB", "en GB", "en-GB-"])
def test_malformed_tags_are_rejected(value):
    assert not LanguageCode.accepts(value)
    with pytest.raises(ValueError):
        LanguageCode(value)


def test_codes_with_the_same_value_are_equal():
    assert LanguageCode("fr") == LanguageCode("fr")
    assert LanguageCode("fr") != LanguageCode("es")
