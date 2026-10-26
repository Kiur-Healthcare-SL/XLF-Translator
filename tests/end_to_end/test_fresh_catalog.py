from xml.etree.ElementTree import fromstring

from support.fixture_documents import FRESH, fixture
from support.real_wiring import opened, wired

from xlf_translator.domain.uploaded_document import UploadedDocument

NAMESPACE = "{urn:oasis:names:tc:xliff:document:1.2}"


def test_the_fresh_fixture_needs_a_language_and_reports_auto_fill():
    _, view = opened(FRESH)
    assert view.classification == "fresh"
    assert view.needs_target_language()
    assert view.auto_filled == (30,)
    assert view.ordinal == 1


def test_a_draft_of_the_fresh_fixture_reopens_as_partial_with_everything_intact():
    use_cases, _ = opened(FRESH)
    use_cases.choose_target_language.execute("en-GB")
    assert use_cases.enter_target.execute("app.title", "CT Scan Analyser").state == "translated"
    draft = use_cases.export_draft.execute()
    assert draft.name == "messages.en-GB.draft.xlf"
    reopened = wired().open_catalog.execute(UploadedDocument(draft.name, draft.content))
    assert reopened.classification == "partial"
    assert (reopened.source_language, reopened.target_language) == ("es", "en-GB")
    assert reopened.ordinal == 2
    original, exported = fromstring(bytes(fixture(FRESH))), fromstring(draft.content)
    for element in ("note", "context-group", "context"):
        assert len(exported.findall(f".//{NAMESPACE}{element}")) == len(original.findall(f".//{NAMESPACE}{element}"))


def test_a_draft_after_ten_translations_carries_eleven_targets():
    use_cases, _ = opened(FRESH)
    use_cases.choose_target_language.execute("en-GB")
    for _ in range(10):
        use_cases.copy_source.execute()
        use_cases.move.forward()
    draft = use_cases.export_draft.execute()
    assert len(fromstring(draft.content).findall(f".//{NAMESPACE}target")) == 11
