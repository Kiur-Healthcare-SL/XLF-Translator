from xlf_translator.domain.catalog_refusal import CatalogRefusal


def test_a_refusal_states_what_was_expected_and_what_was_found():
    refusal = CatalogRefusal("XLIFF version 1.2", "version 2.0")
    assert str(refusal) == "Expected XLIFF version 1.2, found version 2.0."


def test_refusals_with_the_same_reason_are_equal():
    assert CatalogRefusal("a", "b") == CatalogRefusal("a", "b")
    assert CatalogRefusal("a", "b") != CatalogRefusal("a", "c")
