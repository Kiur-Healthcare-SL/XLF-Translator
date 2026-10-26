from support.content_samples import BOLD_PHRASE, CLOSE_BOLD, OPEN_BOLD, content

from xlf_translator.domain.content import Content
from xlf_translator.domain.text_run import TextRun


class Recorder:
    def __init__(self):
        self.written = []

    def text(self, text):
        self.written.append(text)

    def placeholder(self, attributes):
        self.written.append(dict(attributes)["id"])


def test_text_only_content_has_no_placeholders():
    assert Content.of_text("Hallazgos").placeholders() == ()


def test_placeholder_only_content():
    only = content(OPEN_BOLD, CLOSE_BOLD)
    assert only.placeholders() == (OPEN_BOLD, CLOSE_BOLD)
    assert not only.is_blank()


def test_literal_markup_is_text():
    literal = Content.of_text("<p><b>Consejo</b></p>")
    assert literal.placeholders() == ()
    assert list(literal) == [TextRun("<p><b>Consejo</b></p>")]


def test_whitespace_only_content_is_blank():
    assert Content.of_text("   ").is_blank()
    assert Content.of_text("  ").is_blank()
    assert Content([]).is_blank()
    assert not Content.of_text(" a ").is_blank()


def test_adjacent_text_runs_merge_and_empty_runs_vanish():
    assert content("a", "", "b", OPEN_BOLD, "") == content("ab", OPEN_BOLD)


def test_content_writes_items_in_order():
    recorder = Recorder()
    BOLD_PHRASE.write_into(recorder)
    assert recorder.written == ["START_BOLD_TEXT", "limited functionality", "CLOSE_BOLD_TEXT"]
