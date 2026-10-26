import pytest
from support.app_driver import position, started, texts, uploaded
from support.fixture_documents import trans_unit, xliff


def test_the_upload_screen_asks_for_a_catalog():
    app = started()
    assert texts(app.title) == ["XLF Translator"]
    assert len(app.file_uploader) == 1


def test_a_valid_catalog_opens_a_session():
    app = uploaded("messages.en-GB.xlf")
    assert texts(app.title) == ["messages.en-GB.xlf"]
    assert position(app) == "Item 31 of 60"


@pytest.mark.parametrize(
    ("content", "reason"),
    [
        (b" " * 4_194_305, "4,194,305 bytes"),
        (b'<?xml version="1.0" encoding="ISO-8859-1"?><xliff version="1.2"/>', "encoding ISO-8859-1"),
        (xliff(trans_unit("a", "x"), file_attributes='target-language="fr"').encode(), "a source language"),
    ],
)
def test_a_refused_document_leaves_no_session_and_shows_why(content, reason):
    app = uploaded("refused.xlf", content)
    assert texts(app.title) == ["XLF Translator"]
    assert reason in app.error[0].value
