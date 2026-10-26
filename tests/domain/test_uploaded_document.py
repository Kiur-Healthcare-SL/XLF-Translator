from xlf_translator.domain.document_size import DocumentSize
from xlf_translator.domain.language_code import LanguageCode
from xlf_translator.domain.uploaded_document import UploadedDocument

ENGLISH = LanguageCode("en-GB")


def test_the_stem_is_taken_from_the_file_name():
    document = UploadedDocument("messages.xlf", b"<xliff/>")
    assert str(document.draft_name(ENGLISH)) == "messages.en-GB.draft.xlf"
    assert str(document.final_name(ENGLISH)) == "messages.en-GB.xlf"


def test_a_re_uploaded_draft_keeps_the_original_stem():
    document = UploadedDocument("messages.en-GB.draft.xlf", b"<xliff/>")
    assert str(document.final_name(ENGLISH)) == "messages.en-GB.xlf"


def test_the_document_measures_its_size():
    assert UploadedDocument("messages.xlf", b"12345").size() == DocumentSize(5)


def test_the_document_yields_its_bytes():
    assert bytes(UploadedDocument("messages.xlf", b"<xliff/>")) == b"<xliff/>"


def test_the_document_renders_as_its_file_name():
    assert str(UploadedDocument("messages.xlf", b"")) == "messages.xlf"


def test_a_re_uploaded_document_renders_under_its_own_name():
    assert str(UploadedDocument("messages.en-GB.draft.xlf", b"")) == "messages.en-GB.draft.xlf"
