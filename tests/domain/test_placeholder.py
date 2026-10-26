from xlf_translator.domain.placeholder import Placeholder
from xlf_translator.domain.placeholder_attributes import PlaceholderAttributes
from xlf_translator.domain.placeholder_name import PlaceholderName


def placeholder(name, *extra):
    return Placeholder(PlaceholderName(name), PlaceholderAttributes((("id", name),) + extra))


class Recorder:
    def placeholder(self, attributes):
        self.attributes = attributes


def test_same_name_and_attributes_are_equal():
    assert placeholder("START_BOLD_TEXT", ("ctype", "x-b")) == placeholder("START_BOLD_TEXT", ("ctype", "x-b"))


def test_different_attributes_differ():
    assert placeholder("START_BOLD_TEXT", ("ctype", "x-b")) != placeholder("START_BOLD_TEXT", ("ctype", "x-i"))


def test_markup_is_the_equivalent_text():
    assert placeholder("CLOSE_BOLD_TEXT", ("equiv-text", "</b>")).markup() == "</b>"


def test_markup_falls_back_to_the_element():
    assert placeholder("LINE_BREAK").markup() == '<x id="LINE_BREAK"/>'


def test_masked_form_is_the_next_token():
    assert placeholder("LINE_BREAK").masked(iter([3])) == "{3}"


def test_a_placeholder_writes_its_attributes_in_order():
    recorder = Recorder()
    placeholder("LINE_BREAK", ("ctype", "lb")).write_into(recorder)
    assert recorder.attributes == (("id", "LINE_BREAK"), ("ctype", "lb"))
