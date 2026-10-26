from xlf_translator.domain.placeholder_attributes import PlaceholderAttributes

BOLD = (("id", "START_BOLD_TEXT"), ("ctype", "x-b"), ("equiv-text", "<b>"))


def test_attributes_keep_their_order():
    assert list(PlaceholderAttributes(BOLD)) == list(BOLD)


def test_order_matters_for_equality():
    assert PlaceholderAttributes(BOLD) == PlaceholderAttributes(BOLD)
    assert PlaceholderAttributes(BOLD) != PlaceholderAttributes(tuple(reversed(BOLD)))


def test_content_type_and_equivalent_text_round_trip():
    restored = PlaceholderAttributes(tuple(PlaceholderAttributes(BOLD)))
    assert dict(restored)["ctype"] == "x-b"
    assert restored.equivalent_text() == "<b>"


def test_equivalent_text_may_be_absent():
    assert PlaceholderAttributes((("id", "LINE_BREAK"),)).equivalent_text() is None
