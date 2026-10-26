import pytest

from xlf_translator.domain.unit_identifier import UnitIdentifier


def test_identifiers_with_the_same_value_are_equal():
    assert UnitIdentifier("viewer.back") == UnitIdentifier("viewer.back")


def test_identifiers_with_different_values_differ():
    assert UnitIdentifier("viewer.back") != UnitIdentifier("viewer.pan")


@pytest.mark.parametrize("value", ["", "   "])
def test_an_empty_identifier_is_rejected(value):
    with pytest.raises(ValueError):
        UnitIdentifier(value)


def test_an_identifier_is_usable_as_a_dictionary_key():
    targets = {UnitIdentifier("viewer.back"): "Back"}
    assert targets[UnitIdentifier("viewer.back")] == "Back"


def test_an_identifier_renders_as_its_value():
    assert str(UnitIdentifier("viewer.back")) == "viewer.back"
