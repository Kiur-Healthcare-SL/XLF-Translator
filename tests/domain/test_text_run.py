from xlf_translator.domain.text_run import TextRun


class Recorder:
    def text(self, text):
        self.written = text


def test_runs_combine_into_one():
    assert TextRun.combined([TextRun("ab"), TextRun("cd")]) == [TextRun("abcd")]


def test_empty_runs_combine_into_nothing():
    assert TextRun.combined([TextRun("")]) == []


def test_braces_are_doubled_when_masked():
    assert TextRun("{serie}_{1}").masked(iter([])) == "{{serie}}_{{1}}"


def test_whitespace_is_blank():
    assert TextRun("  \n").is_blank()
    assert not TextRun(" a ").is_blank()


def test_a_run_writes_its_text():
    recorder = Recorder()
    TextRun("<p>").write_into(recorder)
    assert recorder.written == "<p>"
