from xlf_translator.domain.placeholder_name import PlaceholderName


def test_names_with_the_same_value_are_equal():
    assert PlaceholderName("START_BOLD_TEXT") == PlaceholderName("START_BOLD_TEXT")
    assert PlaceholderName("START_BOLD_TEXT") != PlaceholderName("CLOSE_BOLD_TEXT")


def test_a_name_renders_as_its_value():
    assert str(PlaceholderName("INTERPOLATION")) == "INTERPOLATION"
